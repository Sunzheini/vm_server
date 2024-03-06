from django.urls import path
from .views import *


"""
Postman:
Headers -> Content-Type -> application/json
Body -> raw -> JSON
{
    "idOfPlcToRequest": "1"
}

{
    "idOfPlcToRequest": "1", 
    "project": 
    {
        "projectname": "Project1", 
        "projectpath": "path...", 
        "githash": "git...", 
        "topologytype": 3, 
        "devicesinthetopology": 
        [
            {
                "deviceid": "1", 
                "ipaddress": "192.168.2.51", 
                "devicetype": "CMMT-AS-MP"
            }, 
            {
                "deviceid": "2", 
                "ipaddress": "192.168.2.52", 
                "devicetype": "CMMT-AS-MP"
            }, 
            {
                "deviceid": "3", 
                "ipaddress": "192.168.2.53", 
                "devicetype": "CMMT-ST-MP"
            }
        ]
    }
}

"""

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
    # Needed to get the vm types for the list of choices when creating a new vm
    # ---------------------------------------------------------------
    # http://127.0.0.1:8000/virtual-machines/vm-types/
    path('vm-types/', VMTypeView.as_view(), name='vm types'),

    # ---------------------------------------------------------------
    # Needed to get the list of plc names
    # ---------------------------------------------------------------
    path('plc-names/', PlcNamesView.as_view(), name='plc names'),

    # ---------------------------------------------------------------
    # Used for the communication with the dll
    # ---------------------------------------------------------------
    # http://127.0.0.1:8000/virtual-machines/request-plc-meta-data/
    path('request-plc-meta-data/', RequestAndResponsePlcMetaDataClassView().as_view(), name='master plc version info exchange'),

    # http://127.0.0.1:8000/virtual-machines/request-plc-configure/
    path('request-plc-configure/', RequestAndResponsePlcConfigureClassView().as_view(), name='master plc configure'),

    # http://127.0.0.1:8000/virtual-machines/request-plc-start/
    path('request-plc-start/', RequestAndResponseStartVmProcessClassView().as_view(), name='request plc start'),
]
