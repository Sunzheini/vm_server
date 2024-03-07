from django.db import models


vm_type_choices = (
    ('TwinCAT', 'TwinCAT'),
    ('TiaPortal', 'TiaPortal'),
    ('Codesys', 'Codesys'),
    ('Studio5000', 'Studio5000'),
)

device_type_choices = (
    ('CMMT-AS-MP', 'CMMT-AS-MP'),
    ('CMMT-ST-MP', 'CMMT-ST-MP'),
)


class VM(models.Model):
    vm_name = models.CharField(max_length=100, unique=True)
    vm_type = models.CharField(max_length=100, choices=vm_type_choices, default='TwinCAT', unique=True)
    selected_plc = models.ForeignKey(
        'Plc',
        on_delete=models.SET_NULL,
        related_name='vms',
        blank=True,
        null=True
    )

    machine_is_started = models.BooleanField(default=False)

    path_to_selected_program = models.CharField(max_length=100, blank=True, null=True)
    name_of_selected_program = models.CharField(max_length=100, blank=True, null=True)

    program_is_open = models.BooleanField(default=False)
    program_is_compiled = models.BooleanField(default=False)
    program_is_downloaded = models.BooleanField(default=False)

    connection_is_online = models.BooleanField(default=False)
    plc_is_running = models.BooleanField(default=False)
    enabled = models.BooleanField(default=False)

    list_of_allowed_functions_for_vm_type = models.TextField(blank=True, null=True)
    list_of_currently_allowed_functions = models.TextField(blank=True, null=True)

    vm_status = models.TextField(blank=True, null=True)
    message_what_changed_last = models.CharField(max_length=100, blank=True, null=True)

    @property
    def define_name_of_selected_program(self):
        try:
            self.name_of_selected_program = self.path_to_selected_program.split('\\')[-1]
        except:
            self.name_of_selected_program = self.path_to_selected_program
        self.save()
        return self.name_of_selected_program

    # @property
    def update_status(self, message_update):
        self.define_name_of_selected_program
        self.message_what_changed_last = message_update

        self.vm_status = ''
        for field in self._meta.get_fields():
            field_name = field.name
            field_value = getattr(self, field_name)
            self.vm_status += f'{field_name}: {field_value}\n'

        self.save()
        return self.vm_status

    def __str__(self):
        return self.vm_name


class Device(models.Model):
    """
    The device object contains the metadata for a specific device. Convention:
    device_type: i.e. CMMT-AS-MP, CMMT-ST-MP
    """
    ip_address = models.GenericIPAddressField(unique=True)
    device_type = models.CharField(max_length=100, choices=device_type_choices)

    def __str__(self):
        return f"Device Id: {self.pk}, IP: {self.ip_address}, Type: {self.device_type}"


class Project(models.Model):
    """
    A project object contains the metadata for a specific project. Convention:
    project_name: i.e. FBW_Beckhoff_Slave_PLC_EtherCAT, FBW_Beckhoff_Master_PLC_EtherCAT
    git_hash: i.e. 123123123, unique hash of the git repository commit
    topology_type: i.e. 1, for now no additional logic is needed
    """
    project_name = models.CharField(max_length=100)
    project_path = models.CharField(max_length=100)
    git_hash = models.CharField(max_length=100, unique=True)
    topology_type = models.PositiveIntegerField(blank=True, null=True)
    devices_in_the_topology = models.ManyToManyField(
        Device,
        related_name='projects',
        blank=True,
        null=True
    )

    def __str__(self):
        return (f"Project Id: {self.pk}, Name: {self.project_name}, Path: {self.project_path}, "
                f"Git hash: {self.git_hash}, Topology type: {self.topology_type}, "
                f"Devices: {[device.ip_address for device in self.devices_in_the_topology.all()]}")


class Plc(models.Model):
    """
    A plc object contains the metadata for a specific plc. Convention:
    plc_type: i.e. CX2030, S7-1500, ControlLogix-1756-L83E, CPX-E-CEC
    vendor_name: i.e. Beckhoff, Siemens, Rockwell, Festo. Using this to link to the virtual machines
    plc_name: i.e. FBW_Beckhoff_Slave_EtherCAT, FBW_Beckhoff_Master_EtherCAT, FBW_Siemens_Slave_Profinet, FBW_Rockwell_Slave_EthernetIP, FBW_Festo_Slave_EtherCAT
    ams_net_id: applicable only for TwinCAT
    ips: 192.168.2.11, 192.168.2.10, 192.168.2.12, 192.168.2.19, 192.168.2.17
    version: i.e. 1
    """
    plc_type = models.CharField(max_length=100)
    vendor_name = models.CharField(max_length=100, choices=vm_type_choices)
    plc_name = models.CharField(max_length=100, unique=True)
    ams_net_id = models.CharField(max_length=100, unique=True, blank=True, null=True)
    ip_address = models.GenericIPAddressField(unique=True)
    version = models.CharField(max_length=100)
    loaded_project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='plcs',
        blank=True,
        null=True
    )

    def __str__(self):
        return (f"PLC Id: {self.pk}, Name: {self.plc_name}, Type: {self.plc_type}, "
                f"AMS Net Id: {self.ams_net_id}, IP: {self.ip_address}, Version: {self.version}, "
                f"Loaded project: {self.loaded_project.project_name}")
