# Generated by Django 5.0.7 on 2024-11-01 02:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_contactus', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contactus',
            options={'ordering': ['id']},
        ),
    ]