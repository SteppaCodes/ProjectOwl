# Generated by Django 4.1.7 on 2023-03-14 17:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0006_alter_milestone_status_alter_project_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worker',
            name='company',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='manager.company'),
        ),
    ]
