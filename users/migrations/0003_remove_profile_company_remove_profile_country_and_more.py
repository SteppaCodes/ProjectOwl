# Generated by Django 4.0 on 2023-03-13 02:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='company',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='country',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='email',
        ),
    ]