# Generated by Django 5.0.7 on 2024-11-01 02:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_custodian', '0018_delete_requestdetailschange'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='branch',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='custodian',
            options={'ordering': ['id']},
        ),
    ]
