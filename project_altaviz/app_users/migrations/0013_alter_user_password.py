# Generated by Django 5.0.7 on 2024-10-16 00:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_users', '0012_engineerassignmentnotificaion_location_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(default='password123', max_length=128),
            preserve_default=False,
        ),
    ]
