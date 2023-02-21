from django.db import models
from enum import Enum
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin


# Create your models here.

SEX = (
    ('Man', 'Male'),
    ('Women', 'Female')
)


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email must be')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(('Superuser must have is_superuser=True.'))

        user = self.create_user(email, password, **extra_fields)
        user.is_admin = True
        user.save()
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=99, verbose_name='Імʼя')
    last_name = models.CharField(max_length=99, null=True, verbose_name='Прізвище')
    email = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    sex = models.CharField(choices=SEX, max_length=10, verbose_name='Стать')
    last_login = models.DateTimeField(auto_now_add=True, null=True, editable=False)
    image = models.ImageField(null=True)
    USERNAME_FIELD = 'email'
    objects = CustomUserManager()

    def __str__(self):
        return f'ID - {self.id}'
