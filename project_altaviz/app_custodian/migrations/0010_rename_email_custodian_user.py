# Generated by Django 5.0.7 on 2024-10-07 22:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_custodian', '0009_rename_custodian_custodian_email_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='custodian',
            old_name='email',
            new_name='user',
        ),
    ]
