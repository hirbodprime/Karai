from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from accounts.managers import CustomUserManager
from django.conf import settings
from django.utils import timezone
import os
import locale

def get_filename_ext(filepath):
    name, ext = os.path.splitext(os.path.basename(filepath))
    return name, ext  


class ImageUploadHandler:
    def __init__(self, folder_name, prefix, type_):
        self.folder_name = folder_name
        self.prefix = prefix
        self.type = type_

    def get_filename(self, instance, filename):
        name, ext = get_filename_ext(filename)
        final_name = f"{self.prefix}-{instance.user}-{ext}"
        return f"users/{instance.user}/data/{self.type}/{self.folder_name}/{final_name}"


class ProfileUploadHandler(ImageUploadHandler):
    def get_filename(self, instance, filename):
        name, ext = get_filename_ext(filename)
        unique_name = str(uuid.uuid4())
        final_name = f"{self.prefix}-{instance.username}-{ext}"
        return f"users/{instance.email}/data/{self.type}/{self.folder_name}/{instance.username}/{final_name}"

upload_profile_image_handler = ProfileUploadHandler('profile_image', 'profile_image', 'profile_images')

def upload_profile_image(instance, filename):
    return upload_profile_image_handler.get_filename(instance, filename)


class CustomUser(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(unique=True,null=True, blank=True)
    username = models.CharField(max_length=30, unique=True, null=True, blank=True)  # Add username field 
    full_name = models.CharField(max_length=60,null=True,blank=True)
    country = models.CharField(max_length=100,null=True,blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    join_date = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    birthday = models.DateField(null=True, blank=True)
    bio = models.CharField(max_length=100, blank=True, null=True)
    profile_image = models.ImageField(upload_to=upload_profile_image,blank=True, null=True) 
    private = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=15, unique=True,blank=True, null=True)
    sms_verification_code = models.CharField(max_length=6, blank=True, null=True)
    is_phone_verified = models.BooleanField(default=False,blank=True, null=True)
    
    objects = CustomUserManager()
    

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['phone_number']  # Add username to REQUIRED_FIELDS
    def __str__(self):
        return f'{self.phone_number}-{self.username}'
    