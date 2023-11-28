from django.contrib import admin

from vm_server.py_terminals.models import PyTerminal
from vm_server.user_management.models import User
from vm_server.virtual_machines.models import VM


admin.site.register(User)
admin.site.register(VM)
admin.site.register(PyTerminal)
