# Generated by Django 5.0.7 on 2024-08-20 08:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_help_desk', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='helpdesk',
            name='is_deleted',
        ),
    ]
