from django.urls import path

from vm_server.main_app.views import (index, test,
                                      get_data, add_item, get_item, delete_item, update_item,
                                      get_users_list, show_user, edit_user, delete_user, add_user,
                                      get_vms_list, show_vm, edit_vm, delete_vm, add_vm,
                                      get_pyterminals_list, show_pyterminal, edit_pyterminal, delete_pyterminal,
                                      add_pyterminal,)

urlpatterns = [
    path('', index, name='index'),
    path('test/', test, name='test'),

    # ---------------------------------------------------------------------------------
    # Test
    # ---------------------------------------------------------------------------------

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

    # ---------------------------------------------------------------------------------
    # User
    # ---------------------------------------------------------------------------------
    # http://127.0.0.1:8000/api/users/users-list/
    path('api/users/users-list/', get_users_list, name='get users list'),

    # http://127.0.0.1:8000/api/users/show-user/1/
    path('api/users/show-user/<str:identifier>/', show_user, name='show user'),

    # http://127.0.0.1:8000/api/users/edit-user/1/
    path('api/users/edit-user/<str:identifier>/', edit_user, name='edit user'),

    # http://127.0.0.1:8000/api/users/delete-user/1/
    path('api/users/delete-user/<str:identifier>/', delete_user, name='delete user'),

    # http://127.0.0.1:8000/api/users/add-user/
    path('api/users/add-user/', add_user, name='add user'),

    # ---------------------------------------------------------------------------------
    # VM
    # ---------------------------------------------------------------------------------
    # http://127.0.0.1:8000/api/vms/vms-list/
    path('api/vms/vms-list/', get_vms_list, name='get vms list'),

    # http://127.0.0.1:8000/api/vms/show-vm/1/
    path('api/vms/show-vm/<str:identifier>/', show_vm, name='show vm'),

    # http://127.0.0.1:8000/api/vms/edit-vm/1/
    path('api/vms/edit-vm/<str:identifier>/', edit_vm, name='edit vm'),

    # http://127.0.0.1:8000/api/vms/delete-vm/1/
    path('api/vms/delete-vm/<str:identifier>/', delete_vm, name='delete vm'),

    # http://127.0.0.1:8000/api/vms/add-vm/
    path('api/vms/add-vm/', add_vm, name='add vm'),

    # ---------------------------------------------------------------------------------
    # PyTerminal
    # ---------------------------------------------------------------------------------
    # http://127.0.0.1:8000/api/pyterm/pyterm-list/
    path('api/pyterm/pyterm-list/', get_pyterminals_list, name='get pyterminals list'),

    # http://127.0.0.1:8000/api/pyterm/show-pyterm/1/
    path('api/pyterm/show-pyterm/<str:identifier>/', show_pyterminal, name='show pyterminal'),

    # http://127.0.0.1:8000/api/pyterm/edit-pyterm/1/
    path('api/pyterm/edit-pyterm/<str:identifier>/', edit_pyterminal, name='edit pyterminal'),

    # http://127.0.0.1:8000/api/pyterm/delete-pyterm/1/
    path('api/pyterm/delete-pyterm/<str:identifier>/', delete_pyterminal, name='delete pyterminal'),

    # http://127.0.0.1:8000/api/pyterm/add-pyterm/
    path('api/pyterm/add-pyterm/', add_pyterminal, name='add pyterminal'),
]
