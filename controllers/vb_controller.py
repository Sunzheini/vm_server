import subprocess
import virtualbox


class VBController:
    """
    This class is responsible for the communication with the VirtualBox.
    You have 2 options for starting and stopping the virtual machine!
    """
    def __init__(self):
        # 1
        self.vbox = None
        self.session = None
        self._create_vbox_object_and_session()

        # 2
        self.machine_object = None
        self.window = None

    # 1
    def _create_vbox_object_and_session(self):
        """
        Creates the vbox and session objects
        """
        self.vbox = virtualbox.VirtualBox()
        self.session = virtualbox.Session()

    # 2
    def _create_machine_object(self, vm_name):
        """
        Creates the machine object
        @param vm_name: the name of the vm
        @return: Success or Machine not found
        """
        try:
            self.machine_object = self.vbox.find_machine(vm_name)
        except virtualbox.library.VBoxErrorObjectNotFound:
            return f"Machine {vm_name} not found"
        return "Success"

    # 2
    def _start_machine_in_window(self):
        """
        Starts the machine in a window
        @return: Success or Exception
        """
        try:
            self.window = self.machine_object.launch_vm_process(self.session, "gui", [])
        except Exception as e:
            return f"Exception: {e}"
        return "Success"

    # 2
    @staticmethod
    def _start_machine_in_window2(vm_name):
        """
        Starts the machine in a window, option 2 using subprocess and vboxmanage
        @param vm_name:
        @return: Success or Error starting Virtual Machine {vm_name}.
        """
        try:
            subprocess.run(['vboxmanage', 'startvm', vm_name], check=True)
        except subprocess.CalledProcessError:
            return f"Error starting Virtual Machine {vm_name}."
        return "Success"

    # 2
    def initiate_machine(self, vm_name):
        """
        Initiates the machine
        @param vm_name: the name of the vm
        """
        result = self._create_machine_object(vm_name)
        if result != "Success":
            return result

        # result = self._start_machine_in_window()
        result = self._start_machine_in_window2(vm_name)
        if result != "Success":
            return result

        return "Success"

    # 3
    def _shutdown_machine(self):
        """
        Shuts down the machine

        VBoxManage controlvm <vm> poweroff: Has the same effect on a virtual
            machine as pulling the power cable on a real computer. The state of the
            VM is not saved beforehand, and data may be lost. This is equivalent to
            selecting the Close item in the Machine menu of the GUI, or clicking the
            VM window's close button, and then selecting Power Off the Machine in
            the displayed dialog.
        @return: Success or Error stopping Virtual Machine {vm_name}.
        """
        try:
            self.session.console.power_down()
            # self._unlock_session()
        except Exception as e:
            return f"Error stopping Virtual Machine {self.machine_object.name}."
        return "Success"

    # 3
    @staticmethod
    def _shutdown_machine2(vm_name):
        """
        Shuts down the machine, option 2 using subprocess and vboxmanage.

        VBoxManage controlvm <vm> savestate: Saves the current state of
            the VM to disk and then stops the VM. This is equivalent to
            selecting the Close item in the Machine menu of the GUI or clicking
            the VM window's close button, and then selecting Save the Machine
            State in the displayed dialog.
        @param vm_name:
        @return: Success or Error stopping Virtual Machine {vm_name}.
        """
        try:
            subprocess.run(['vboxmanage', 'controlvm', vm_name, 'savestate'], check=True)
        except subprocess.CalledProcessError:
            return f"Error stopping Virtual Machine {vm_name}."
        return "Success"

    # 3
    def _unlock_session(self):
        self.session.unlock_machine()

    # 3
    def _lock_session(self):
        self.machine_object.lock_machine(self.session, virtualbox.library.LockType.shared)

    # 3
    def power_down(self, vm_name):
        """
        Shuts down the machine
        @return: Success or Error stopping Virtual Machine {vm_name}.
        """
        result = self._shutdown_machine2(vm_name)
        if result != "Success":
            return result

        return "Success"

