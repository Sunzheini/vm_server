from controllers.vb_controller import VBController
from vm_server.settings import virtual_machine_name, location_of_server_code_folder


"""
This is the instance of the VBController class.
"""


vb_controller = VBController(virtual_machine_name, location_of_server_code_folder)
print("vb_controller initiated")
print(vb_controller)
