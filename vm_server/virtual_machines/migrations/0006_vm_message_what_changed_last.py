# Generated by Django 4.2.4 on 2023-11-28 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('virtual_machines', '0005_remove_vm_name_of_previous_selected_program_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='vm',
            name='message_what_changed_last',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
