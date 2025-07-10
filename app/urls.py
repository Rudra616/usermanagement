from django.urls import path
from  .views import *
urlpatterns = [
    path('register/',register, name='register'),
    path('login/',login,name='login'),
    path('test-logging/', test_log, name='test_log'),

    path('update_profile/', update_profile, name='update_profile'),
    path('delete_user/<int:id>/', delete_user, name='delete_user'),  
    path('verify/<uuid:token>/', verify_email, name='verify_email'),
    path('get-districts/', get_districts, name='get_districts'),  # ✅ ADD THIS
    path('refresh-captcha/', refresh_captcha, name='refresh_captcha'),

    path('logout',logout,name='logout'),
    # path('home',home,name='home'),
    path('user_listing',admin_dashbord,name='admin_dashbord'),
    path('forgot-password/', forgot_password_view, name='forgot_password'),
    path('reset-password/<uuid:token>/',reset_password_view, name='reset_password'),
    # boostrep teamplates
    path('',index,name="index"),
    path('about/',about,name="about"),
    path('feature/',feature,name="feature"),
    path('service/',service,name="service"),
    path('team/',team,name="team"),
    path('testimonial/',testimonial,name="testimonial"),
    path('appoinment/',appoinment,name="appoinment"),
    path('error/',error,name="error"),
    path('contact/',contact,name="contact")



]

