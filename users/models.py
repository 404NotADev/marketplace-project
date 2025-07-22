import uuid

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from .send_email import send_activation_email


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.create_activation_code()
        send_activation_email(user.email, user.activation_code)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        if not email:
            raise ValueError('email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class UserModel(AbstractUser): #
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, blank=True)
    biouser = models.TextField(blank=True)
    is_active = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=300, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def create_activation_code(self):
        code = str(uuid.uuid4())
        self.activation_code = code

    def __str__(self):
        return f'{self.email}'
