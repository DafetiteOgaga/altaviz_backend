# Generated by Django 5.0.7 on 2024-11-03 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_users', '0023_updatelocationandbranchnotification_approve_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='updatelocationandbranchnotification',
            name='approved_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='updatelocationandbranchnotification',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
