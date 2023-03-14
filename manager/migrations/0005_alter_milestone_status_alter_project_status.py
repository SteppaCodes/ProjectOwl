# Generated by Django 4.0 on 2023-03-13 23:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0004_alter_company_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='milestone',
            name='status',
            field=models.CharField(choices=[('In Progress', 'In Progress'), ('In Qeue', 'In Qeue'), ('Paused', 'Paused'), ('Completed', 'Completed')], default='In Qeue', max_length=200),
        ),
        migrations.AlterField(
            model_name='project',
            name='status',
            field=models.CharField(choices=[('In Progress', 'In Progress'), ('In Qeue', 'In Qeue'), ('Paused', 'Paused'), ('Completed', 'Completed')], default='In Qeue', max_length=200),
        ),
    ]