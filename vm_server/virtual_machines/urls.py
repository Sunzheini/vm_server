from django.urls import path

from .views import *


urlpatterns = [
    # http://127.0.0.1:8000/virtual-machines/vms-list/
    path('vms-list/', get_vms_list, name='get vms list'),

    # http://127.0.0.1:8000/virtual-machines/add-vm/
    path('add-vm/', add_vm, name='add vm'),

    # http://127.0.0.1:8000/virtual-machines/show-vm/1/
    path('show-vm/<str:identifier>/', show_vm, name='show vm'),

    # http://127.0.0.1:8000/virtual-machines/edit-vm/1/
    path('edit-vm/<str:identifier>/', edit_vm, name='edit vm'),

    # http://127.0.0.1:8000/virtual-machines/delete-vm/1/
    path('delete-vm/<str:identifier>/', delete_vm, name='delete vm'),

    # ---------------------------------------------------------------

    # http://127.0.0.1:8000/virtual-machines/vm-types/
    path('vm-types/', VMTypeView.as_view(), name='vm types')
]
