# Generated by Django 5.0.7 on 2024-12-26 18:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_bank', '0006_alter_bank_options_alter_state_options'),
        ('app_custodian', '0021_alter_branch_branch_engineer'),
        ('app_location', '0013_alter_location_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branch',
            name='bank',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='bankbranches', to='app_bank.bank'),
        ),
        migrations.AlterField(
            model_name='branch',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='locationbranches', to='app_location.location'),
        ),
    ]