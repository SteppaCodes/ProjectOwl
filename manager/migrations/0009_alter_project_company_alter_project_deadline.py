# Generated by Django 4.1.7 on 2023-03-14 19:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0008_alter_company_company_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='company',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='manager.company'),
        ),
        migrations.AlterField(
            model_name='project',
            name='deadline',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
    ]