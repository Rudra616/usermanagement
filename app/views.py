from django.shortcuts import render,redirect,get_object_or_404
from .models import user,District,State
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import uuid
# from django.shortcuts import get_object_or_404
from django.db.models import Q

from django.core.mail import EmailMultiAlternatives
from django.core.paginator import Paginator

from django.http import JsonResponse

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        email = request.POST.get('email', '').strip()
        number = request.POST.get('number', '').strip()
        firstname = request.POST.get('FirstName', '').strip()
        lastname = request.POST.get('LastName', '').strip()
        address = request.POST.get('address', '').strip()
        district_id = request.POST.get('district', '').strip()
        state_id = request.POST.get('state', '').strip()
        date_of_birth = request.POST.get('date_of_birth','').strip()        
        if not all([username, password, email, number, firstname, lastname, address, district_id, state_id]):
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': 'All fields are required.'})
            else:
                return render(request, 'reg_user.html')
        if user.objects.filter(username=username).exists():
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': 'Username already taken.'})
            else:
                return render(request, 'reg_user.html', {'error': 'Username already taken.'})

        image = request.FILES.get('image')
        email_verification_token = uuid.uuid4()

        data = user()
        data.firstName = firstname
        data.lastName = lastname
        data.username = username
        data.password = password
        data.email = email
        data.phone_number = number
        data.image = image
        data.address = address
        data.district = District.objects.get(pk=district_id)
        data.state = State.objects.get(pk=state_id)
        data.role = 'user'
        data.date_of_birth = date_of_birth
        data.email_verification_token = email_verification_token
        data.is_varified = False
        data.save() 

        verification_link = request.build_absolute_uri(f'/verify/{email_verification_token}/')

        convert_to_html_content = render_to_string("email.html", {
            'verificationtoken': verification_link
        })

        plain_msg = strip_tags(convert_to_html_content)    
        subject ='subject here'
        from_email = settings.EMAIL_HOST_USER
        to_email = [data.email]
        email_message = EmailMultiAlternatives(subject, plain_msg, from_email, to_email)
        email_message.attach_alternative(convert_to_html_content,'text/html')
        email_message.send(fail_silently=True)

        return JsonResponse({'success': True, 'message': 'Registration successful. Please verify your email.'})
    
    # GET request – pass state list to template
    states = State.objects.all()
    return render(request, 'reg_user.html', {'states': states})


# AJAX endpoint to fetch districts
def get_districts(request):
    state_id = request.GET.get('state_id')
    districts = District.objects.filter(state_id=state_id).values('id', 'name')
    return JsonResponse(list(districts), safe=False)


def admin_dashbord(request):
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
        if per_page == 'all':
            per_page_count = all_users.count()
        else:
            per_page_count = int(per_page)
        page_number = request.GET.get("page")
        #  get the page number next click then page 2 show o
        #  Give me the users for this page number.
        paginator = Paginator(all_users,per_page_count)
        #  paginator was devide the page large to small picess
        #  show all user perpage count how many user you want to show this see 
        page_obj = paginator.get_page(page_number)
        matched_page= None
        #  no matched page
        if search_query:
            #  serch any username 
            full_users = user.objects.filter(role='user').order_by('id')
            #  This gets all users with role = 'user', sorted by their ID (not username).
            match =full_users.filter(username__icontains=search_query).first()
            #  This finds the first user whose username contains the search word.
            if match:
                postion = list(full_users).index(match)
                #  Converts the full queryset (full_users) into a list.
                #  if find the user
                matched_page = postion // per_page_count + 1 if per_page != 'all' else 1
                #  It calculates on which page the matched user appears.
                #  suppose postion was 20 
                #  page par count you select = 10 
                #  matched_page = 22 // 10 + 1
                #   = 2 + 1
                #   = 3
                #   in if condition go not all then claculation 
                #   if all then return 1                    
        context = {
            'userdetails': user_obj,
            'is_admin': True,
            'users': page_obj,
            "search_query": search_query,
            'per_page': per_page,
            'matched_page': matched_page,
            'search_count': search_count if search_query else None

        }

        # If it's AJAX request, return only HTML table part
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            html = render_to_string("user_table.html", context)
            return JsonResponse({"html": html})

        return render(request, 'admin.html', context)
def login(request):
    if request.method == 'POST':
        userName = request.POST['name']
        password = request.POST['password']

        user_obj = user.objects.filter(username=userName).first()

        if user_obj:
            if password == user_obj.password:
                if not user_obj.is_varified:
                    return render(request, 'login.html', {'error3': 'Please verify your email first.'})
                
                # ✅ Only set session AFTER verified
                request.session['username'] = user_obj.username

                if user_obj.role == 'admin':
                    return redirect('admin_dashbord')
                else:
                    return redirect('index')
            else:
                return render(request, 'login.html', {'error': 'Wrong password'})
        else:
            return render(request, 'login.html', {'error1': 'User name not found'})       

    return render(request, 'login.html')

def update_profile(request):
    userName = request.session.get('username')
    user_obj = user.objects.filter(username=userName).first()
    
    if request.method == 'POST':
        new_username = request.POST['username']

        already_user = user.objects.filter(username=new_username).first()

        if already_user:
            if already_user.id != user_obj.id:
                return render(request, 'user_profile.html', {
                    'username': user_obj,
                    'error': 'Username already taken.'
                })
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
                
        messages.success(request, 'Profile updated successfully.')

        return redirect('update_profile') 
        

    return render(request, 'user_profile.html', {
        'username': user_obj
    })

def delete_user(request,id):
    try:
        user_to_delete = user.objects.get(id=id)  
        user_to_delete.delete()                  
    except user.DoesNotExist:
        print("User not found")
    return redirect('admin_dashboard')






# Vefiy User Account  
def verify_email(request, token):
    try:
        user_obj = user.objects.get(email_verification_token=token)
    except user.DoesNotExist:
        user_obj = user.objects.filter(is_varified=True).first()
        if user_obj:
            messages.info(request,"the varification link already varified")
            return redirect('login')
        else:          
            messages.error(request, "Invalid or expired verification link.")
            return redirect('login')  # or an error page
    # Check if already verified
        
    if user_obj.is_varified:
        messages.info(request, "Your email is already verified.")
        # Automatically log the user in
        request.session['username'] = user_obj.username
        return redirect('index')  # or wherever you want to send the user

    # Mark as verified
    user_obj.is_varified = True
    user_obj.email_verification_token = None  # This ensures the token is removed
    user_obj.save()

    messages.success(request, "Your email has been verified. You can now log in.")
    return redirect('login')


def logout(request):
    if 'username' in request.session:
        del request.session['username']  
    return redirect('index')  

# def home(request):
#     userName = request.session.get('username')
#     user_obj = user.objects.filter(username=userName).first()
#     return render(request, 'home.html', {'userdetails': user_obj, 'is_admin': False})

def forgot_password_view(request):
    message = ""
    if request.method == 'POST':
        username = request.POST.get('username')
        User = user.objects.filter(username=username).first()
        if User:
            token = uuid.uuid4()
            User.reset_token = token
            User.reset_expire = timezone.now() + timezone.timedelta(hours=1)
            User.save()
            reset_link = request.build_absolute_uri(f'/reset-password/{token}/')
            send_mail(
                'Password Reset',
                f'Reset your password using this link: {reset_link}',
                settings.EMAIL_HOST_USER,
                [User.email],
                fail_silently=False,
            )
        # Show message regardless of username validity
        message = "If the username exists, a reset link has been sent to the registered email."

    return render(request, 'forgot_password.html', {'message': message})
from django.utils import timezone
def reset_password_view(request, token):
    User = get_object_or_404(user, reset_token=token, reset_expire__gt=timezone.now())
    # get_object_or_404 work like try catch excpetion
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm = request.POST.get('confirm_password')

        if password == confirm:
            User.password = password  
            User.reset_token = None
            User.reset_expire = None
            User.save()
            return redirect('login')
        else:
            return render(request, 'reset_password.html', {'error': 'Passwords do not match.'})

    return render(request, 'reset_password.html')



def index(request):
    return render(request,'index.html')

def about(request):
    return render(request, 'about.html')

def feature(request):
    return render(request, 'feature.html')

def service(request):
    return render(request, 'service.html')

def team(request):
    return render(request, 'team.html')

def testimonial(request):
    return render(request, 'testimonial.html')

def appoinment(request):
    return render(request, 'appoinment.html')


def error(request):
    return render(request, '404.html')
def contact(request):
    return render(request, 'contact.html')