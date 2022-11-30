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

    def user_is_staff(self):
        if self.role == 'Admin':
            return self.is_staff

    def __str__(self):
        return self.username
