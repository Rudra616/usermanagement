from django.urls import path
from  .views import *

urlpatterns = [
    path('reg',register, name='register'),
    path('',login,name='login'),
    path('update_profile', update_profile, name='update_profile'),
    path('delete_user/<int:id>/', delete_user, name='delete_user'),  

]


# def register(request):
#     if request.method=='POST':
#         username = request.POST['username']
#         if user.objects.filter(username=username).exists():
#             return render(request,'reg_user.html',{'error':'Username already taken.'})

    
#         FirstName = request.POST.get('FirstName')
#         LastName = request.POST.get['LastName']
#         username = username
#         password = request.POST.get['password'] 
#         email = request.POST.get['email']
#         phonenumber = request.POST.get['number']
#         image = request.FILES.get.get['password'] 
#         address = request.POST.get['address']
#         district = request.POST.get['district']
#         state = request.POST.get['state']
#         role = 'user'
#         user.objects.create(FirstName=FirstName,LastName=LastName,password=password,username=username,email=email,phonenumber=phonenumber,image=image,address=address,district=district,state=state,role=role)
#         user.save()
#         return render(request, 'reg_user.html',{'success': 'User registered successfully.'})
#     return render(request, 'reg_user.html')


# if user_data.role != selected_role:
#             return render(request, 'login.html', {'error': 'Role mismatch. Please select the correct role.'})
#         request.session['user_id'] = user_data.id
#         if user.role == 'admin':
#             return redirect('admin_dashboard')
#         else:
#             return redirect('user_dashboard')