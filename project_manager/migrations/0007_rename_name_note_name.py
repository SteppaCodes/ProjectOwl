# Generated by Django 4.1.7 on 2023-03-18 20:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project_manager', '0006_note'),
    ]

    operations = [
        migrations.RenameField(
            model_name='note',
            old_name='Name',
            new_name='name',
        ),
    ]