# Generated by Django 5.0.7 on 2024-08-07 15:30

import app_users.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_users', '0002_alter_user_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_picture',
            field=models.ImageField(blank=True, default='profile_pictures/placeholder.png', null=True, upload_to=app_users.models.unique_profile_pic),
        ),
    ]
