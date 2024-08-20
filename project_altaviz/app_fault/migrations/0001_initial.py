# Generated by Django 5.0.7 on 2024-08-20 04:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app_bank', '0001_initial'),
        ('app_engineer', '0002_initial'),
        ('app_help_desk', '0002_initial'),
        ('app_supervisor', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fault',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('atm_number', models.IntegerField()),
                ('status', models.BooleanField(default=False)),
                ('confirm_resolve', models.BooleanField(default=False)),
                ('verify_resolve', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('resolved_at', models.DateTimeField(auto_now=True)),
                ('assigned_to', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='assignedTo', to='app_engineer.engineer')),
                ('logged_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='loggedBy', to='app_bank.bank')),
                ('managed_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='managedBy', to='app_help_desk.helpdesk')),
                ('supervised_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='supervisedBy', to='app_supervisor.supervisor')),
            ],
        ),
    ]
