# Generated by Django 5.0.7 on 2024-10-09 23:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_custodian', '0013_rename_engineer_branch_branch_engineer'),
    ]

    operations = [
        migrations.RenameField(
            model_name='requestdetailschange',
            old_name='user',
            new_name='custodian',
        ),
    ]