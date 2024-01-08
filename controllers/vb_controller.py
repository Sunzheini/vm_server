from time import sleep
import virtualbox

from core.decorators import time_measurement_decorator


class VBController:
    """
    This class is responsible for the communication with the VirtualBox
    """
    def __init__(self, machine_name, location_of_server):
        self.machine_name = machine_name

        self.vbox = None
        self.session = None
        self.machine_object = None

        self.progress = None

        self.location_of_server = location_of_server
        self.first_server_command = f"cd {self.location_of_server}"
        self.second_server_command = f"python main.py"

    def _create_vbox_object_and_session(self):
        self.vbox = virtualbox.VirtualBox()
        self.session = virtualbox.Session()
        sleep(1)

    def _create_machine_object(self):
        try:
            self.machine_object = self.vbox.find_machine(self.machine_name)
        except virtualbox.library.VBoxErrorObjectNotFound:
            print(f"Machine {self.machine_name} not found")
        sleep(1)

    @time_measurement_decorator
    def initiate(self):
        self._create_vbox_object_and_session()
        self._create_machine_object()

    def print_list_of_vms(self):
        print([m.name for m in self.vbox.machines])

    def check_states(self):
        current_machine_state = self.machine_object.state
        current_session_state = self.session.state
        print("----------------------------------------------------")
        print(f"Machine state: {current_machine_state}, Session state: {current_session_state}")
        print("----------------------------------------------------")
        print()

    def unlock_session(self):
        self.session.unlock_machine()

    def lock_session(self):
        self.machine_object.lock_machine(self.session, virtualbox.library.LockType.shared)

    @time_measurement_decorator
    def start_machine_in_window(self):
        self.progress = self.machine_object.launch_vm_process(self.session, "gui", [])

        self.progress.wait_for_completion(timeout=-1)  # -1 means wait indefinitely
        if self.progress.result_code != 0:
            raise Exception(f'Failed to start machine: {self.progress.error_info.text}')

    @time_measurement_decorator
    def send_kb_command_for_log_in(self):
        self.send_kb_command("q\n")
        sleep(2)
        self.send_kb_command("pass\n")
        sleep(2)

    @time_measurement_decorator
    def send_kb_command(self, command):
        self.session.console.keyboard.put_keys(command + "\n")
        sleep(2)

    @time_measurement_decorator
    def power_down(self):
        # hard shutdown
        self.session.console.power_down()

        # Send ACPI power button event: currently ACPI not working
        """
        self.session.console.power_button()

        while self.machine_object.state != virtualbox.library.MachineState.powered_off:
            sleep(1)
        """

        self.unlock_session()
