# Generated by Django 5.0.7 on 2024-10-13 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_location', '0008_alter_location_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='location',
            field=models.CharField(max_length=200),
        ),
    ]