# Generated by Django 5.0.7 on 2024-11-03 19:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_location', '0009_alter_location_location'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='location',
            options={'ordering': ['id']},
        ),
    ]