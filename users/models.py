from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name='почта')
    fullname = models.CharField(max_length=150, verbose_name='ФИО')
    phone = models.CharField(max_length=50, verbose_name='номер телефона', null=True, blank=True)
    token = models.CharField(max_length=100, verbose_name='токен', null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.fullname} - {self.email}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        permissions = [
            ('view_all_users', 'Can view all users'),
            ('deactivate_user', 'Can deactivate users'),
        ]
