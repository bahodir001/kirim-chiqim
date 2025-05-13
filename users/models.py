from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
import random
# from django.contrib.auth import get_user_model
#
#
# User = get_user_model()

class EmailVerification(models.Model):
    email = models.EmailField()
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.email} - {self.code}"


class CustomUserManager(BaseUserManager):
    def create_user(self, email, phone_number, first_name, last_name, card_number, password=None):
        if not email:
            raise ValueError("Email is required")
        user = self.model(
            email=self.normalize_email(email),
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
            card_number=card_number,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone_number, first_name, last_name, card_number, password=None):
        user = self.create_user(email, phone_number, first_name, last_name, card_number, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    card_number = models.CharField(max_length=20)

    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
    family_group = models.ForeignKey('FamilyGroup', on_delete=models.SET_NULL, null=True, blank=True)
    role_in_family = models.CharField(max_length=10, choices=[('admin', 'Admin'), ('member', 'Member')], default='member')

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'  
    REQUIRED_FIELDS = ['phone_number', 'first_name', 'last_name', 'card_number']

    def __str__(self):
        return self.email


class FamilyGroup(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
