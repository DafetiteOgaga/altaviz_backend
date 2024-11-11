# Generated by Django 5.0.7 on 2024-10-03 23:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_bank', '0005_state_region'),
        ('app_location', '0004_alter_location_region'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='location',
            name='bank',
        ),
        migrations.AddField(
            model_name='location',
            name='bank',
            field=models.ManyToManyField(blank=True, null=True, related_name='banklocations', to='app_bank.bank'),
        ),
    ]