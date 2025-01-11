from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from datetime import timezone

GENDER_CHOICES = [
    ('male', 'Male'),
    ('female', 'Female'),
]

class CustomUserManager(BaseUserManager):
    def deactivate_user(self, user):
        user.is_active = False
        user.save()

        return user

    def create_user(self, email, password, **other_fields):
        if not email:
            raise ValueError("Email Address must be provided")
        if not password:
            raise ValueError("Password Address must be provided")
        
        other_fields.setdefault('is_active', True)
        email = self.normalize_email(email)
        user = self.model(email=email, **other_fields)
        user.set_password(password)
        user.save()        

        return user
    
    def create_superuser(self, email, password, **otherfields):
        otherfields.setdefault('is_staff', True)
        otherfields.setdefault('is_superuser', True)

        return self.create_user(email, password, **otherfields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    photo = models.ImageField(upload_to='users/%Y/%m/%d', null=True)
    bio = models.CharField(max_length=500, null=True)
    email = models.EmailField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateField(auto_now_add = True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=100, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)


    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    def __str__(self) -> str:
        return self.email    
    