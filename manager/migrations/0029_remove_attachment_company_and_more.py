# Generated by Django 4.1.7 on 2023-03-16 15:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0028_alter_attachment_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attachment',
            name='company',
        ),
        migrations.RemoveField(
            model_name='attachment',
            name='milestone',
        ),
        migrations.RemoveField(
            model_name='attachment',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='attachment',
            name='project',
        ),
        migrations.RemoveField(
            model_name='attachment',
            name='task',
        ),
        migrations.RemoveField(
            model_name='milestone',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='milestone',
            name='project',
        ),
        migrations.RemoveField(
            model_name='milestone',
            name='updated_by',
        ),
        migrations.RemoveField(
            model_name='project',
            name='company',
        ),
        migrations.RemoveField(
            model_name='project',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='project',
            name='teams',
        ),
        migrations.RemoveField(
            model_name='project',
            name='updated_by',
        ),
        migrations.RemoveField(
            model_name='task',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='task',
            name='milestone',
        ),
        migrations.RemoveField(
            model_name='task',
            name='workers',
        ),
        migrations.DeleteModel(
            name='Activity',
        ),
        migrations.DeleteModel(
            name='Attachment',
        ),
        migrations.DeleteModel(
            name='MileStone',
        ),
        migrations.DeleteModel(
            name='Project',
        ),
        migrations.DeleteModel(
            name='Task',
        ),
    ]