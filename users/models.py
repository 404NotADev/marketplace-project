import uuid
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
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

        UserActionLog.objects.create(
            user=user,
            action='register',
            description='Пользователь зарегистрировался'
        )

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

        UserActionLog.objects.create(
            user=user,
            action='create_superuser',
            description='Создан суперпользователь'
        )

        return user


class UserModel(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, blank=True)
    biouser = models.TextField(blank=True)
    is_active = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=300, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def create_activation_code(self):
        self.activation_code = str(uuid.uuid4())

    def __str__(self):
        return f'{self.email}'


class UserActionLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.user.email} - {self.action} at {self.timestamp}'
