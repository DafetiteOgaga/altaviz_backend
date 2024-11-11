# Generated by Django 5.0.7 on 2024-10-07 00:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_location', '0006_alter_location_bank'),
        ('app_users', '0002_rename_date_of_birth_user_dob'),
    ]

    operations = [
        migrations.AlterField(
            model_name='engineer',
            name='location',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='app_location.location'),
        ),
    ]
