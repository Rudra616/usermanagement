from django.contrib import admin

# Register your models here.
from .models import user

class appadmin(admin.ModelAdmin):
    list_display = ['FirstName','LastName','username','password','email','address','state','role','district','image','phonenumber']
admin.site.register(user)