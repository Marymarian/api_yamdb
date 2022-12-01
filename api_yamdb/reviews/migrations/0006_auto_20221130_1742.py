# Generated by Django 2.2.16 on 2022-11-30 14:42

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0005_auto_20221130_1739'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='username',
            field=models.CharField(max_length=150, unique=True, validators=[django.core.validators.RegexValidator(message='Имя пользователя должно содержать толькобуквы, цифры или @/./+/-/_ ', regex='^[\\w.@+-]+$')], verbose_name='Имя пользователя'),
        ),
    ]