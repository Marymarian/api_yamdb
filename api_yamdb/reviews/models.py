from django.db import models

from django.contrib.auth.models import AbstractUser

ROLE_CHOICES = (
               ('User', 'Пользователь'),
               ('Moderator', 'Модератор'),
               ('Admin', 'Администратор'),
)


class Users(AbstractUser):
    bio = models.TextField(blank=True, verbose_name='О себе')
    role = models.CharField(choices=ROLE_CHOICES, max_length=16,
                            default='User', verbose_name='Роль')

    def __str__(self):
        return self.username
