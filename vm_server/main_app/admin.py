from django.contrib import admin
from vm_server.main_app.models import User, VM, PyTerminal


admin.site.register(User)
admin.site.register(VM)
admin.site.register(PyTerminal)
