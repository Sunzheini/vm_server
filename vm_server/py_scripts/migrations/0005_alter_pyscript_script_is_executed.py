# Generated by Django 4.2.4 on 2023-11-30 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('py_scripts', '0004_alter_pyscript_script_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pyscript',
            name='script_is_executed',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
