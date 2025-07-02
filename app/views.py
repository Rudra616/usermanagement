from django.shortcuts import render,redirect
from .models import user
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
        district = request.POST.get('district', '').strip()
        state = request.POST.get('state', '').strip()
        
        if not all([username, password, email, number, firstname, lastname, address, district, state]):
            return render(request, 'reg_user.html')


        if user.objects.filter(username=username).exists():
            return render(request, 'reg_user.html', {'error': 'Username already taken.'})
        email_verification_token = uuid.uuid4()

        image = request.FILES.get('image')
        data = user()
        data.firstName = firstname
        data.lastName = lastname
        data.username = username
        data.password = password
        data.email = email
        data.phone_number = number
        data.image = image
        data.address = address
        data.district = district
        data.state = state
        data.role = 'user'
        data.email_verification_token = email_verification_token
        data.is_varified = False
        data.save() 

        verification_link = request.build_absolute_uri(f'/verify/{email_verification_token}/')

        convert_to_html_content = render_to_string("email.html",{'varifictiontoken':verification_link}
        )
        plain_msg = strip_tags(convert_to_html_content)    
        subject ='subject here'
        from_email = settings.EMAIL_HOST_USER
        to_email = [data.email]
        email_message = EmailMultiAlternatives(subject, plain_msg, from_email, to_email)

        email_message.attach_alternative(convert_to_html_content,'text/html')
        email_message.send(fail_silently=True)
        
        messages.success(request, "Registration successful.")
        return redirect('register')
        


    return render(request, 'reg_user.html')


# def admin_dashboard(request):
#     username = request.session.get('username')
#     if not username:
#         return redirect('login')

#     user_obj = user.objects.filter(username=username).first()
#     if not user_obj or user_obj.role != 'admin':
#         return redirect('login') 

#     # search_query = request.GET.get('search', '')

  
#     all_users = user.objects.filter(role='user')

#     # if search_query:
#     #     all_users = all_users.filter(
#     #         Q(username__icontains=search_query) |
#     #         Q(firstName__icontains=search_query) |
#     #         Q(lastName__icontains=search_query) |
#     #         Q(email__icontains=search_query) |
#     #         Q(address__icontains=search_query) |
#     #         Q(district__icontains=search_query) |
#     #         Q(state__icontains=search_query)
#     #     )

#     page_number = request.GET.get("page")
#     paginator = Paginator(all_users,10)
#     page_obj = paginator.get_page(page_number)
#     return render(request, 'admin.html', {
#         'admin_name': user_obj.username,
#         'users': page_obj
#     })

def login(request):
    if request.method == 'POST':
        userName = request.POST['name']
        password = request.POST['password']

        user_obj = user.objects.filter(username=userName).first()

        if user_obj:
            if password == user_obj.password:
                request.session['username'] = user_obj.username  
                if not user_obj.is_varified:
                    return render(request, 'login.html', {'error3': 'Please verify your email first.'})
                else: 
                        if user_obj.role == 'admin':
                            # all_users = user.objects.filter(role='user')
                            return redirect('home')
                        else:
                            # return render(request, 'user_profile.html', {
                            #     'username': user_obj
                            # })
                            return redirect('home')
            else:
                return render(request, 'login.html', {'error': 'Wrong password'})
        else:
            return render(request, 'login.html', {'error1': 'user name not found'})       
    return render(request,'login.html')

# def login(request):
#     if request.method == 'POST':
#         userName = request.POST.get('name')
#         password = request.POST.get('password')

#         user_obj = user.objects.filter(username=userName).first()

#         if user_obj:
#             if password == user_obj.password:
#                 if not user_obj.is_varified:
#                     if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#                         return JsonResponse({'error': 'Please verify your email first.', 'type': 'error3'})
#                     return render(request, 'login.html', {'error3': 'Please verify your email first.'})
#                 else:
#                     request.session['username'] = user_obj.username
#                     if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#                         return JsonResponse({'success': True, 'redirect': '/home'})  # or use reverse()
#                     return redirect('home')
#             else:
#                 if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#                     return JsonResponse({'error': 'Wrong password', 'type': 'error'})
#                 return render(request, 'login.html', {'error': 'Wrong password'})
#         else:
#             if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#                 return JsonResponse({'error': 'Username not found', 'type': 'error1'})
#             return render(request, 'login.html', {'error1': 'Username not found'})       

#     return render(request, 'login.html')


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
        return redirect('home')  # or wherever you want to send the user

    # Mark as verified
    user_obj.is_varified = True
    user_obj.email_verification_token = None  # This ensures the token is removed
    user_obj.save()

    messages.success(request, "Your email has been verified. You can now log in.")
    return redirect('login')


def logout(request):
    if 'username' in request.session:
        del request.session['username']  
    return redirect('home')  

def home(request):
    userName = request.session.get('username')
    user_obj = user.objects.filter(username=userName).first()
    
    if user_obj and user_obj.role == 'admin':
        all_users = user.objects.filter(role='user')

        search_query = request.GET.get('search', '')

        if search_query:
            all_users = all_users.filter(
            username__icontains=search_query 
            )

        per_page = request.GET.get("per_page","10")

        if per_page == 'all':
            per_page_count = all_users.count()
        else:
            per_page_count = int(per_page)
        page_number = request.GET.get("page")
        #  get the page number next click then page 2 show o
        paginator = Paginator(all_users,per_page_count)
        #  paginator was devide the page large to small picess
        #  show all user perpage count how many user you want to show this see 
        page_obj = paginator.get_page(page_number)
        #  Give me the users for this page number.
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
        return render(request, 'home.html', {
            'userdetails': user_obj,
            'is_admin': True,  
            'users': page_obj,   
            "search_query":search_query,
            'per_page': per_page,          
            'matched_page': matched_page 
        })  
    
    return render(request, 'home.html', {'userdetails': user_obj, 'is_admin': False})


def index(request):
    return render(request,'index.html')