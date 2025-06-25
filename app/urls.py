from django.urls import path
from  .views import *

urlpatterns = [
    path('register/',register, name='register'),
    path('login/',login,name='login'),
    path('update_profile/', update_profile, name='update_profile'),
    path('delete_user/<int:id>/', delete_user, name='delete_user'),  
    path('admin_dashboard',admin_dashboard,name='admin_dashboard'),
    path('verify/<uuid:token>/', verify_email, name='verify_email'),
    path('logout',logout,name='logout'),
    path('home',home,name='home')
]

