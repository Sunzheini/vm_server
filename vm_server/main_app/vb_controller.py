from time import sleep
import virtualbox


virtual_machine_name = 'VM000180'
location_of_server_code_folder = 'C:\\Users\\User\\Desktop\\server_code'
# url_of_server_on_vm = 'http://192.168.56.101:5000/command'
# url_of_server_on_vm = 'http://127.0.0.1:5000/command'  # home
url_of_server_on_vm = 'http://172.23.139.29:5000/command'  # when on festo wifi and after changing the ip of the vm
location_for_the_log_file = 'log.txt'


class VBController:
    _VB_OBJECT = None
    _SESSION = None
    _MACHINE_OBJECT = None
    _PROGRESS = None

    def _create_vbox_object_and_session(self):
        self._VB_OBJECT = virtualbox.VirtualBox()
        self._SESSION = virtualbox.Session()
        sleep(1)

    def _create_machine_object(self, machine_name):
        try:
            _MACHINE_OBJECT = self._VB_OBJECT.find_machine(machine_name)
        except virtualbox.library.VBoxErrorObjectNotFound:
            print(f"Machine {machine_name} not found")
        sleep(1)

    def initiate(self):
        self._create_vbox_object_and_session()
        self._create_machine_object(virtual_machine_name)

    def start_machine_in_window(self):
        self._PROGRESS = (self._MACHINE_OBJECT
                          .launch_vm_process(self._SESSION, "gui", []))

        self._PROGRESS.wait_for_completion(timeout=-1)  # -1 means wait indefinitely
        if self._PROGRESS.result_code != 0:
            raise Exception(f'Failed to start machine: '
                            f'{self._PROGRESS.error_info.text}')
