from django.urls import path

from .newViews import *


urlpatterns = [
    path('new_index/', new_index, name='new_index'),
    path('logout/', logout_user, name='new_logout'), 
    path('verify/<uuid:token>/', new_verify_email, name='new_verify_email'),
]