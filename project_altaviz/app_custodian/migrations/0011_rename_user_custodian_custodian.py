# Generated by Django 5.0.7 on 2024-10-07 22:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_custodian', '0010_rename_email_custodian_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='custodian',
            old_name='user',
            new_name='custodian',
        ),
    ]