# Generated by Django 5.0.7 on 2024-10-11 07:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_fault', '0005_fault_resolved_by'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fault',
            old_name='resolved_by',
            new_name='replacement_engineer',
        ),
    ]