# Generated by Django 5.0.7 on 2025-01-01 22:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_inventory', '0006_alter_component_options_alter_componentname_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='unconfirmedpart',
            name='name2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='fixedpartnames', to='app_inventory.partname'),
        ),
    ]
