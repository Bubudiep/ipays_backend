# Generated by Django 5.0.3 on 2024-03-08 01:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ipays', '0004_rename_users_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Photos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('file_type', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('file_size', models.IntegerField(blank=True, null=True)),
                ('img', models.BinaryField(blank=True, null=True)),
                ('Comment', models.CharField(blank=True, default='', max_length=1024)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(blank=True, default='', max_length=100)),
                ('adr_tinh', models.CharField(blank=True, default='', max_length=100)),
                ('adr_thanhpho', models.CharField(blank=True, default='', max_length=100)),
                ('adr_huyen', models.CharField(blank=True, default='', max_length=100)),
                ('adr_xa', models.CharField(blank=True, default='', max_length=100)),
                ('Comment', models.CharField(blank=True, default='', max_length=1024)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]