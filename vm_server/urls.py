from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('vm_server.main_app.urls')),

    path('user-management/', include('vm_server.user_management.urls')),
    path('virtual-machines/', include('vm_server.virtual_machines.urls')),
    path('py-terminals/', include('vm_server.py_terminals.urls')),
]
