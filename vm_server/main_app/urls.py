from django.urls import path

from vm_server.main_app.views import index


urlpatterns = [
    path('', index, name='index'),
]
