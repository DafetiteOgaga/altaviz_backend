# Generated by Django 5.0.7 on 2024-10-01 11:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_bank', '0004_rename_intials_state_initial'),
        ('app_users', '0002_rename_date_of_birth_user_dob'),
    ]

    operations = [
        migrations.AddField(
            model_name='state',
            name='region',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='regionstates', to='app_users.region'),
        ),
    ]
