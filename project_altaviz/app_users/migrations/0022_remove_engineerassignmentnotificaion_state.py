# Generated by Django 5.0.7 on 2024-11-02 09:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_users', '0021_engineerassignmentnotificaion_state'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='engineerassignmentnotificaion',
            name='state',
        ),
    ]