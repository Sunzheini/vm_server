from django.urls import path

from vm_server.main_app.views import index, test, get_data, add_item, get_item, delete_item, update_item

urlpatterns = [
    path('', index, name='index'),
    path('test/', test, name='test'),

    # http://127.0.0.1:8000/api/
    path('api/', get_data, name='get data'),

    # http://127.0.0.1:8000/api/get/2/
    # http://127.0.0.1:8000/api/get/Item2/
    path('api/get/<str:identifier>/', get_item, name='get item'),

    # http://127.0.0.1:8000/api/add/
    path('api/add/', add_item, name='add item'),

    # http://127.0.0.1:8000/api/delete/1/
    # http://127.0.0.1:8000/api/get/2/
    # http://127.0.0.1:8000/api/get/Item2/
    path('api/delete/<str:identifier>/', delete_item, name='delete_item'),

    # http://127.0.0.1:8000/api/update/2/
    # http://127.0.0.1:8000/api/update/Item2/
    path('api/update/<int:identifier>/', update_item, name='update_item'),
]
