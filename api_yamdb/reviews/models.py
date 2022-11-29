from django.db import models

from django.contrib.auth.models import AbstractUser

ROLE_CHOICES = (
               ('User', 'Пользователь'),
               ('Moderator', 'Модератор'),
               ('Admin', 'Администратор'),
)


class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True,
                                verbose_name='Имя пользователя')
    email = models.EmailField(max_length=254, unique=True,
                              verbose_name='Электронная почта')
    first_name = models.CharField(max_length=150, blank=True,
                                  verbose_name='Имя')
    last_name = models.CharField(max_length=150, blank=True,
                                 verbose_name='Фамилия')
    bio = models.TextField(blank=True, verbose_name='О себе')
    role = models.CharField(choices=ROLE_CHOICES, max_length=16,
                            default='User', verbose_name='Роль')

    def __str__(self):
        return self.username


class Titles(models.Model):
    title = models.CharField(max_length=150)


class Categories(models.Model):
    title = models.CharField(max_length=150)


class Genres(models.Model):
    title = models.CharField(max_length=150)


class Reviews(models.Model):
    title = models.CharField(max_length=150)


class Comments(models.Model):
    title = models.CharField(max_length=150)
