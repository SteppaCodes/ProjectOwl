# Generated by Django 4.1.7 on 2023-03-15 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0019_task_created_task_updated'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('In Progress', 'In Progress'), ('In Queue', 'In Queue'), ('Paused', 'Paused'), ('Completed', 'Completed')], default='In Queue', max_length=200),
        ),
    ]
