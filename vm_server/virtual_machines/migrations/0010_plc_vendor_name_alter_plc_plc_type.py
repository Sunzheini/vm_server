# Generated by Django 4.2.4 on 2024-03-05 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('virtual_machines', '0009_alter_project_project_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='plc',
            name='vendor_name',
            field=models.CharField(choices=[('TwinCAT', 'TwinCAT'), ('TiaPortal', 'TiaPortal'), ('Codesys', 'Codesys'), ('Studio5000', 'Studio5000')], default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='plc',
            name='plc_type',
            field=models.CharField(max_length=100),
        ),
    ]
