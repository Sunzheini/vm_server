from controllers.vb_controller import VBController


virtual_machine_name = 'VM000180'
location_of_server_code_folder = 'C:\\Users\\User\\Desktop\\server_code'


"""
This is the instance of the VBController class.
"""


vb_controller = VBController(virtual_machine_name, location_of_server_code_folder)
print("vb_controller initiated")
print(vb_controller)
