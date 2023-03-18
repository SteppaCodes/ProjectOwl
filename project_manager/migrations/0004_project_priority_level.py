# Generated by Django 4.1.7 on 2023-03-18 02:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_manager', '0003_attachment_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='priority_level',
            field=models.CharField(choices=[('Normal', 'Normal'), ('ASAP', 'ASAP')], default='Normal', max_length=100),
        ),
    ]