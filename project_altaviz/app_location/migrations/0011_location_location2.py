# Generated by Django 5.0.7 on 2024-11-03 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_location', '0010_alter_location_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='location2',
            field=models.CharField(blank=True, max_length=200, null=True, unique=True),
        ),
    ]