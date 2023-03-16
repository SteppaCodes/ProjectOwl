# Generated by Django 4.1.7 on 2023-03-16 03:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0024_remove_activity_team'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='team',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='manager.team'),
        ),
    ]
