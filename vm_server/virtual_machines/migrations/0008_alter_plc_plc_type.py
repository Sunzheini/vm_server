# Generated by Django 4.2.4 on 2024-02-22 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('virtual_machines', '0007_device_project_plc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plc',
            name='plc_type',
            field=models.CharField(choices=[('TwinCAT', 'TwinCAT'), ('TiaPortal', 'TiaPortal'), ('Codesys', 'Codesys'), ('Studio5000', 'Studio5000')], max_length=100),
        ),
    ]
