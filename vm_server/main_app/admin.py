from django.contrib import admin

from vm_server.user_management.models import User
from vm_server.virtual_machines.models import VM
from vm_server.py_scripts.models import PyScript
from vm_server.py_terminals.models import PyTerminal


admin.site.register(User)
admin.site.register(VM)
admin.site.register(PyScript)
admin.site.register(PyTerminal)
