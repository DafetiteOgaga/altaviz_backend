# Generated by Django 5.0.7 on 2024-08-20 05:55

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_bank', '0005_alter_custodian_email'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='custodian',
            name='email',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='mail', to=settings.AUTH_USER_MODEL),
        ),
    ]