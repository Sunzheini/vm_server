from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('vm_server.main_app.urls')),
    path('user-management/', include('vm_server.user_management.urls')),
    path('virtual-machines/', include('vm_server.virtual_machines.urls')),
    path('py-scripts/', include('vm_server.py_scripts.urls')),
    path('py-terminals/', include('vm_server.py_terminals.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
