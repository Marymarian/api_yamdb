# Generated by Django 2.2.16 on 2022-11-30 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0006_auto_20221130_1742'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='username',
            field=models.CharField(max_length=150, unique=True, verbose_name='Имя пользователя'),
        ),
    ]