# Generated by Django 5.0.7 on 2024-09-29 13:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app_bank', '0001_initial'),
        ('app_location', '0001_initial'),
        ('app_users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='region',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='app_users.region'),
        ),
        migrations.AddField(
            model_name='location',
            name='state',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='statelocations', to='app_bank.state'),
        ),
    ]