# Generated by Django 5.0.7 on 2024-11-03 17:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_custodian', '0020_alter_branch_branch_engineer'),
        ('app_users', '0024_alter_updatelocationandbranchnotification_approved_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branch',
            name='branch_engineer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='branchengineer', to='app_users.engineer'),
        ),
    ]
