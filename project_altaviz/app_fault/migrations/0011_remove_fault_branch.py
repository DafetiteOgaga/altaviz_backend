# Generated by Django 5.0.7 on 2024-12-29 07:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_fault', '0010_fault_branch'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fault',
            name='branch',
        ),
    ]