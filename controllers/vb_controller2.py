import subprocess
from time import sleep

"""
terminal:
https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/vboxmanage-controlvm.html

VBoxManage startvm VM000180        # start - working
VBoxManage controlvm VM000180 poweroff      # hard poweroff - working
VBoxManage controlvm VM000180 acpipowerbutton    # soft poweroff with ACPI - not working

VBoxManage controlvm VM000180 savestate     # save state - working
"""



def start_vm(vm_name):
    try:
        subprocess.run(['vboxmanage', 'startvm', vm_name], check=True)
        print(f"Virtual Machine {vm_name} started successfully.")
    except subprocess.CalledProcessError:
        print(f"Error starting Virtual Machine {vm_name}.")

def stop_vm(vm_name):
    try:
        """
        VBoxManage controlvm <vm> savestate: Saves the current state of 
        the VM to disk and then stops the VM. This is equivalent to 
        selecting the Close item in the Machine menu of the GUI or clicking 
        the VM window's close button, and then selecting Save the Machine 
        State in the displayed dialog.
        """
        subprocess.run(['vboxmanage', 'controlvm', vm_name, 'savestate'], check=True)
        print(f"Virtual Machine {vm_name} stopped successfully.")
    except subprocess.CalledProcessError:
        print(f"Error stopping Virtual Machine {vm_name}.")

# Replace 'VM000180' with the actual name of your Virtual Machine
vm_name = 'VM000180'

# Start the Virtual Machine
start_vm(vm_name)

sleep(60)

# Stop the Virtual Machine
stop_vm(vm_name)

"""
VBoxManage controlvm <vm> poweroff: Has the same effect on a virtual 
machine as pulling the power cable on a real computer. The state of the 
VM is not saved beforehand, and data may be lost. This is equivalent to 
selecting the Close item in the Machine menu of the GUI, or clicking the 
VM window's close button, and then selecting Power Off the Machine in 
the displayed dialog.
"""
