# Generated by Django 4.1.7 on 2023-03-18 22:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('project_manager', '0008_alter_task_created_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='created_by',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]