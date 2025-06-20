from django.shortcuts import render,redirect
from .models import user

def register(request):
    if request.method=='POST':
        username = request.POST['username']
        if user.objects.filter(username=username).exists():
            return render(request,'reg_user.html',{'error':'Username already taken.'})
        image = request.FILES.get('image')
        data = user()
        data.FirstName = request.POST['FirstName']
        data.LastName = request.POST['LastName']
        data.username = username
        data.password = request.POST['password'] 
        data.email = request.POST['email']
        data.phonenumber = request.POST['number']
        data.image = image
        data.address = request.POST['address']
        data.district = request.POST['district']
        data.state = request.POST['state']
        data.role = 'user'
        data.save()
        print("name",data.FirstName)
        return render(request, 'reg_user.html',{'success': 'User registered successfully.'})
    return render(request, 'reg_user.html')


def login(request):
    if request.method == 'POST':
        userName = request.POST['name']
        password = request.POST['password']

        user_obj = user.objects.filter(username=userName).first()

        if user_obj:
            if password == user_obj.password:
                request.session['username'] = user_obj.username  

                if user_obj.role == 'admin':
                    all_users = user.objects.filter(role='user')
                    return render(request, 'admin.html', {
                        'admin_name': user_obj.username,
                        'users': all_users
                    })


                else:
                    return render(request, 'user_profile.html', {
                        'username': user_obj
                    })
            else:
                return render(request, 'login.html', {'error': 'Wrong password'})
        else:
            return render(request, 'login.html', {'error1': 'Username not found'})

    return render(request, 'login.html')

def update_profile(request):
    userName = request.session.get('username')
    user_obj = user.objects.filter(username=userName).first()
    
    if request.method == 'POST':
        new_username = request.POST['username']
        if user.objects.filter(username=new_username).exists():
            return render(request, 'user_profile.html', {
                'username': user_obj,
                'error': 'Username already taken.'
        })
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
            
  

        user_obj.save()

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

    return redirect('login')