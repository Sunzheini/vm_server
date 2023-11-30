from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import *


urlpatterns = [
    # http://127.0.0.1:8000/py-scripts/py-scripts-list/
    path('py-scripts-list/', get_py_scripts_list, name='get py_scripts list'),

    # http://127.0.0.1:8000/py-scripts/add-py-script/
    path('add-py-script/', add_py_script, name='add py_script'),

    # http://127.0.0.1:8000/py-scripts/show-py-script/1/
    path('show-py-script/<str:identifier>/', show_py_script, name='show py_script'),

    # http://127.0.0.1:8000/py-scripts/edit-py-script/1/
    path('edit-py-script/<str:identifier>/', edit_py_script, name='edit py_script'),

    # http://127.0.0.1:8000/py-scripts/delete-py-script/1/
    path('delete-py-script/<str:identifier>/', delete_py_script, name='delete py_script'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
