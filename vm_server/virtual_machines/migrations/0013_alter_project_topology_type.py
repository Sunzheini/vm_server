# Generated by Django 4.2.4 on 2024-03-05 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('virtual_machines', '0012_alter_project_topology_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='topology_type',
            field=models.PositiveIntegerField(blank=True, default=1, null=True),
        ),
    ]
