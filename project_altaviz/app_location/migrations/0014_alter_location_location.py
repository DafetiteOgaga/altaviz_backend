# Generated by Django 5.0.7 on 2024-12-27 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_location', '0013_alter_location_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='location',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
