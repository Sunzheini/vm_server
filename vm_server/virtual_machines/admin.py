from django.contrib import admin

from vm_server.virtual_machines.models import VM, Device, Project, Plc


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    pass


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    pass


@admin.register(Plc)
class PlcAdmin(admin.ModelAdmin):
    pass

