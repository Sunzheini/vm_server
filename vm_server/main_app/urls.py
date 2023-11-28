from django.urls import path
from vm_server.main_app.views import *


urlpatterns = [
    # http://127.0.0.1:8000/login/
    path('login/', LoginView.as_view(), name='login'),
]
