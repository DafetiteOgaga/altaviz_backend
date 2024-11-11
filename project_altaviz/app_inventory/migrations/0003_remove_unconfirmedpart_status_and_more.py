# Generated by Django 5.0.7 on 2024-10-06 21:16

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_inventory', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='unconfirmedpart',
            name='status',
        ),
        migrations.AddField(
            model_name='unconfirmedpart',
            name='approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='unconfirmedpart',
            name='approved_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='unconfirmedpart',
            name='rejected',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='unconfirmedpart',
            name='requested_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]