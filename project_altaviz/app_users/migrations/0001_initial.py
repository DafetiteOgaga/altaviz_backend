# Generated by Django 5.0.7 on 2024-08-20 04:56

import app_users.models
import django.contrib.auth.models
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app_department', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('middle_name', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.EmailField(max_length=200, unique=True)),
                ('username', models.CharField(blank=True, max_length=30, null=True)),
                ('password', models.CharField(max_length=128)),
                ('phone', models.CharField(max_length=15)),
                ('wphone', models.CharField(max_length=15)),
                ('address', models.CharField(max_length=200)),
                ('deliveries', models.IntegerField(default=0)),
                ('pendings', models.IntegerField(default=0)),
                ('profile_picture', models.ImageField(blank=True, default='profile_pictures/placeholder.png', null=True, upload_to=app_users.models.unique_profile_pic)),
                ('aboutme', models.TextField(blank=True, null=True)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='departments', to='app_department.department')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
