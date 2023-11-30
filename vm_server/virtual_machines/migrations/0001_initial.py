# Generated by Django 4.2.4 on 2023-11-24 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='VM',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vm_name', models.CharField(max_length=100, unique=True)),
                ('vm_status', models.TextField(blank=True, null=True)),
                ('is_started', models.BooleanField(default=False)),
                ('is_compiled', models.BooleanField(default=False)),
                ('is_downloaded', models.BooleanField(default=False)),
                ('is_online', models.BooleanField(default=False)),
                ('is_running', models.BooleanField(default=False)),
                ('is_enabled', models.BooleanField(default=False)),
                ('param_name', models.CharField(blank=True, max_length=100, null=True)),
                ('param_value', models.CharField(blank=True, max_length=100, null=True)),
                ('is_read', models.BooleanField(default=False)),
            ],
        ),
    ]