# Generated by Django 5.0.7 on 2024-10-15 22:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_users', '0008_remove_user_deliveries'),
    ]

    operations = [
        migrations.CreateModel(
            name='EngineerAssignmentNotificaion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=False)),
                ('supervisor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_users.engineer')),
            ],
        ),
    ]
