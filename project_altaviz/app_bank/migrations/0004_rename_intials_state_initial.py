# Generated by Django 5.0.7 on 2024-09-29 16:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_bank', '0003_rename_key_state_intials'),
    ]

    operations = [
        migrations.RenameField(
            model_name='state',
            old_name='intials',
            new_name='initial',
        ),
    ]
