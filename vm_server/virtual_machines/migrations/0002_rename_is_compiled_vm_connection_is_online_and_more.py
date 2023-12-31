# Generated by Django 4.2.4 on 2023-11-27 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('virtual_machines', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vm',
            old_name='is_compiled',
            new_name='connection_is_online',
        ),
        migrations.RenameField(
            model_name='vm',
            old_name='is_downloaded',
            new_name='enabled',
        ),
        migrations.RenameField(
            model_name='vm',
            old_name='is_enabled',
            new_name='machine_is_started',
        ),
        migrations.RenameField(
            model_name='vm',
            old_name='is_online',
            new_name='param_is_read',
        ),
        migrations.RenameField(
            model_name='vm',
            old_name='is_read',
            new_name='param_is_written',
        ),
        migrations.RenameField(
            model_name='vm',
            old_name='is_running',
            new_name='plc_is_running',
        ),
        migrations.RenameField(
            model_name='vm',
            old_name='is_started',
            new_name='program_is_compiled',
        ),
        migrations.AddField(
            model_name='vm',
            name='list_of_allowed_functions_for_vm_type',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='vm',
            name='list_of_currently_allowed_functions',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='vm',
            name='name_of_previous_selected_program',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='vm',
            name='name_of_selected_program',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='vm',
            name='param_type',
            field=models.CharField(choices=[('Bool', 'Bool'), ('Int', 'Int'), ('Real', 'Real'), ('String', 'String')], default='Int', max_length=100),
        ),
        migrations.AddField(
            model_name='vm',
            name='path_to_previous_selected_program',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='vm',
            name='path_to_selected_program',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='vm',
            name='program_is_downloaded',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='vm',
            name='program_is_open',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='vm',
            name='vm_previous_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='vm',
            name='vm_type',
            field=models.CharField(choices=[('TwinCAT', 'TwinCAT'), ('TiaPortal', 'TiaPortal'), ('Codesys', 'Codesys'), ('Studio5000', 'Studio5000')], default='TwinCAT', max_length=100),
        ),
    ]
