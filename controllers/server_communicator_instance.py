from controllers.server_communicator import ServerCommunicator
from vm_server.settings import url_of_server_on_vm


"""
This file is used to create a ServerCommunicator instance.
"""

srv_communicator = ServerCommunicator(url_of_server_on_vm)
print("srv_communicator initiated")
print(srv_communicator)
