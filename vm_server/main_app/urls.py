from django.urls import path

from vm_server.main_app.views import index, test


urlpatterns = [
    path('', index, name='index'),
    path('/test', test, name='test'),
]
