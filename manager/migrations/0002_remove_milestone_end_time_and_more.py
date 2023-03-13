# Generated by Django 4.0 on 2023-03-13 21:56

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='milestone',
            name='end_time',
        ),
        migrations.RemoveField(
            model_name='milestone',
            name='pause_time',
        ),
        migrations.RemoveField(
            model_name='milestone',
            name='start_time',
        ),
        migrations.RemoveField(
            model_name='milestone',
            name='time_spent',
        ),
        migrations.AddField(
            model_name='task',
            name='end_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='name',
            field=models.CharField(default='New Task', max_length=200),
        ),
        migrations.AddField(
            model_name='task',
            name='pause_time',
            field=models.DurationField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='start_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='time_spent',
            field=models.DurationField(default=datetime.timedelta(0)),
        ),
        migrations.AlterField(
            model_name='company',
            name='company_key',
            field=models.CharField(default='0000', max_length=200),
        ),
        migrations.AlterField(
            model_name='team',
            name='head',
            field=models.OneToOneField(blank=True, default='No Head', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='head', to='manager.worker'),
        ),
        migrations.AlterField(
            model_name='worker',
            name='company',
            field=models.ForeignKey(blank=True, default='Company Not Set', null=True, on_delete=django.db.models.deletion.CASCADE, to='manager.company'),
        ),
    ]
