# Generated by Django 5.0.7 on 2024-10-07 09:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_custodian', '0006_remove_custodian_email_custodian_branch_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='custodian',
            old_name='custodian',
            new_name='email',
        ),
    ]
