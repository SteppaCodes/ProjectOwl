# Generated by Django 4.1.7 on 2023-03-14 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0007_alter_worker_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='company_key',
            field=models.CharField(default=None, max_length=200),
        ),
    ]
