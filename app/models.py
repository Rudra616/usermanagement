from django.db import models

# Create your models here.
import uuid

class user(models.Model):
    option = [
        ('user','User'),
        ('admin','Admin')
    ]
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    username = models.CharField(max_length=50 , unique=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    password = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    address = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    role = models.CharField(max_length=50, choices=option, default='user')
    district = models.CharField(max_length=50)
    image = models.ImageField(upload_to="user_images/", blank=True)
    is_varified =models.BooleanField(default=False)
    email_verification_token = models.UUIDField(default=uuid.uuid4, unique=True, null=True, blank=True)
    def __str__(self):
        return self.username


