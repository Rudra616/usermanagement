from django.shortcuts import render,redirect
from .models import user
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags



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


        image = request.FILES.get('image')
        data = user()
        data.FirstName = firstname
        data.LastName = lastname
        data.username = username
        data.password = password
        data.email = email
        data.phonenumber = number
        data.image = image
        data.address = address
        data.district = district
        data.state = state
        data.role = 'user'

        template_name="email.html"
        convert_to_html_content = render_to_string(
            template_name=template_name,
        )
        plain_msg = strip_tags(convert_to_html_content)


        
        send_mail(
            'subject here',
            plain_msg,
            settings.EMAIL_HOST_USER,
            [data.email],
            fail_silently=True
        )
        data.save()        
        messages.success(request, "Registration successful.")
        return redirect('register')
        


    return render(request, 'reg_user.html')

def admin_dashboard(request):
    username = request.session.get('username')
    if not username:
        return redirect('login')

    user_obj = user.objects.filter(username=username).first()
    if not user_obj or user_obj.role != 'admin':
        return redirect('login') 

    all_users = user.objects.filter(role='user')
    return render(request, 'admin.html', {
        'admin_name': user_obj.username,
        'users': all_users
    })

def login(request):
    if request.method == 'POST':
        userName = request.POST['name']
        password = request.POST['password']

        user_obj = user.objects.filter(username=userName).first()

        if user_obj:
            if password == user_obj.password:
                request.session['username'] = user_obj.username  

                if user_obj.role == 'admin':
                    # all_users = user.objects.filter(role='user')
                    return redirect('admin_dashboard')


                else:
                    # return render(request, 'user_profile.html', {
                    #     'username': user_obj
                    # })
                    return redirect('update_profile')
            else:
                return render(request, 'login.html', {'error': 'Wrong password'})
        else:
            return render(request, 'login.html', {'error1': 'user name not found'})
           
    return render(request,'login.html')


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
        user_obj.FirstName = request.POST['FirstName']
        user_obj.LastName = request.POST['LastName']
        user_obj.email = request.POST['email']
        user_obj.phonenumber = request.POST['number']
        user_obj.address = request.POST['address']
        user_obj.password = request.POST['password']
        user_obj.district = request.POST['district']
        user_obj.state = request.POST['state']
        image = request.FILES.get('image')  
        if image:
            user_obj.image = image 
        # request.session['username'] = user_obj.username



        user_obj.save()

        request.session['username'] = user_obj.username

        return render(request, 'user_profile.html', {
            'username': user_obj,
            'success': 'Profile updated successfully.'
        })
        

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


def home(request):

    return render(request,'home.html')