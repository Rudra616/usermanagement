from django.shortcuts import render, redirect
from django.contrib import messages
from .models import user
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
import uuid
from django.core.paginator import Paginator

def new_index(request):
    user_obj = None
    error = None
    success_message = None
    section = 'login'  # default section

    page_obj = None
    search_query = ''
    per_page = '10'
    matched_page = None
    search_count = None

    if request.session.get("username"):
        user_obj = user.objects.filter(username=request.session["username"]).first()
        section = 'home'

    if request.method == 'POST':
        action = request.POST.get('action')
        
        # LOGIN
        if action == 'login':
            username = request.POST.get('name', '').strip()
            password = request.POST.get('password', '').strip()
            print("login")
            user_obj = user.objects.filter(username=username).first()

            if user_obj:
                if user_obj.password == password:
                    if not user_obj.is_varified:
                        error = "Please verify your email before logging in."
                        section = 'login'
                    else:
                        request.session['username'] = user_obj.username
                        return redirect('new_index')
                else:
                    error = "Incorrect password."
                    section = 'login'
            else:
                error = "Username not found."
                section = 'login'

        # REGISTER
        elif action == 'register':
            username = request.POST.get('username', '').strip()
            password = request.POST.get('password', '').strip()
            email = request.POST.get('email', '').strip()
            number = request.POST.get('number', '').strip()
            firstname = request.POST.get('FirstName', '').strip()
            lastname = request.POST.get('LastName', '').strip()
            address = request.POST.get('address', '').strip()
            district = request.POST.get('district', '').strip()
            state = request.POST.get('state', '').strip()
            image = request.FILES.get('image')

            # Validation
            if not all([username, password, email, number, firstname, lastname, address, district, state]):
                error = "All fields are required."
                section = 'register'
            elif user.objects.filter(username=username).exists():
                error = "Username already exists."
                section = 'register'
            else:
                email_verification_token = uuid.uuid4()
                new_user = user(
                    firstName=firstname,
                    lastName=lastname,
                    username=username,
                    password=password,
                    email=email,
                    phone_number=number,
                    image=image,
                    address=address,
                    district=district,
                    state=state,
                    role='user',
                    email_verification_token=email_verification_token,
                    is_varified=False
                )
                new_user.save()

                # Send verification email
                verification_link = request.build_absolute_uri(f'/verify/{email_verification_token}/')
                html_content = render_to_string("email.html", {'verificationtoken': verification_link})
                plain_msg = strip_tags(html_content)
                subject = 'Verify your email'
                from_email = settings.EMAIL_HOST_USER
                to_email = [new_user.email]
                email_message = EmailMultiAlternatives(subject, plain_msg, from_email, to_email)
                email_message.attach_alternative(html_content, 'text/html')
                email_message.send(fail_silently=True)

                success_message = "Registration successful. Check your email to verify your account."
                section = 'register'

        elif action == 'update_profile':
            userName = request.session.get('username')
            user_obj = user.objects.filter(username=userName).first()
            section = 'update_profile'
            if request.method == 'POST':
                new_username = request.POST['username']

                already_user = user.objects.filter(username=new_username).first()

                if already_user:
                    if already_user.id != user_obj.id:
                        messages.error(request, "All fields are required.")
                        section = 'update_profile'
                user_obj.username = new_username
                user_obj.firstName = request.POST['FirstName']
                user_obj.lastName = request.POST['LastName']
                user_obj.email = request.POST['email']
                user_obj.phone_number = request.POST['number']
                user_obj.address = request.POST['address']
                user_obj.password = request.POST['password']
                user_obj.district = request.POST['district']
                user_obj.state = request.POST['state']
                image = request.FILES.get('image')  
                if image:
                    user_obj.image = image 


                user_obj.save()

                request.session['username'] = user_obj.username


                messages.success(request, "updated successfully")
                section = 'update_profile'

        elif section == 'admin_deshbord':
            print("helo")
            userName = request.session.get('username')
            user_obj = user.objects.filter(username=userName).first()
            if user_obj and user_obj.role == 'admin':

                all_users = user.objects.filter(role='user')
                search_query = request.GET.get('search', '')

                if search_query:
                    all_users = all_users.filter(
                    username__icontains=search_query 
                )
                search_count = all_users.count()

                sort = request.GET.get('sort','')
                if sort == 'username':
                    all_users = all_users.order_by('username')


                per_page = request.GET.get("per_page","10")
                try:
                    per_page_count = int(per_page) if per_page != 'all' else all_users.count()
                except ValueError:
                    per_page_count = 10
                page_number = request.GET.get("page")
                paginator = Paginator(all_users,per_page_count)
               
                page_obj = paginator.get_page(page_number)            
                matched_page= None
                if search_query:
                    full_users = user.objects.filter(role='user').order_by('id')
                    match =full_users.filter(username__icontains=search_query).first()
                    if match:
                        postion = list(full_users).new_index(match)
                        matched_page = postion // per_page_count + 1 if per_page != 'all' else 1
             
    return render(request, "new_usermanagement/new_index.html", {
        "section": section,
        "userdetails": user_obj,
        "error": error,
        "success_message": success_message,       
        'userdetails': user_obj,
        'is_admin': True,
        'users': page_obj,
        "search_query": search_query,
        'per_page': per_page,
        'matched_page': matched_page,
        'search_count': search_count if search_query else None

            
    })

def logout_user(request):
    if 'username' in request.session:
        del request.session['username']  
    return redirect('new_index')

def new_verify_email(request, token):
    try:
        user_obj = user.objects.get(email_verification_token=token)
        if user_obj.is_varified:
            messages.info(request, "Your email is already verified.")
        else:
            user_obj.is_varified = True
            user_obj.email_verification_token = None
            user_obj.save()
            messages.success(request, "Your email has been verified. You can now log in.")
    except user.DoesNotExist:
        messages.error(request, "Invalid or expired verification link.")

    return redirect('new_index')
