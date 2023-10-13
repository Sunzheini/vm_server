from django.contrib import admin
from vm_server.main_app.models import Item, User, VM, PyTerminal


admin.site.register(Item)
admin.site.register(User)
admin.site.register(VM)
admin.site.register(PyTerminal)
