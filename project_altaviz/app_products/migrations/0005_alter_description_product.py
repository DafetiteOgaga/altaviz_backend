# Generated by Django 5.0.7 on 2024-08-07 14:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_products', '0004_remove_product_descriptions_description_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='description',
            name='product',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app_products.product'),
        ),
    ]