from vm_server.virtual_machines.models import Project, Device


class EntityToDbObjectTranslator:
    """
    This class is responsible for creating a database object from an entity from the .NET DLLs. The `entities`
    are the names of the classes in the dll, which define the structure of the data, i.e. the `Device`
    and the `Plc` class.
    """
    @staticmethod
    def _check_if_device_is_in_the_db(device_id):
        """
        Check if the device is in the database
        @param device_id: string
        @return: bool
        """
        try:
            Device.objects.get(pk=device_id)
            return True
        except Device.DoesNotExist:
            return False

    @staticmethod
    def create_db_object_from_project_entity(dll_runner, project_entity):
        """
        Create a new project from the project entity and save it to the database.
        1. Get the project name, project path, git hash, and topology type from the project entity
        2. Create a dictionary with .NET objects from the list of devices in the topology
        3. Translate the dictionary to dict with python objects
        4. Create a new project object
        5. Manage the devices in the topology
        6. Save the new project object to the database
        @param dll_runner: the object of the DllRunner class
        @param project_entity: the object of the Project class of the .NET DLLs
        @return: object of Project model
        """
        # 1
        project_name, project_path, git_hash, topology_type = (
            project_entity.ProjectName,
            project_entity.ProjectPath,
            project_entity.GitHash,
            project_entity.TopologyType,
        )

        # 2
        devices_in_the_topology_python_list_with_dll_objects = dll_runner.translate_dotnet_generic_list_to_python_list(
            project_entity.ListOfDevicesInTheTopology,
        )
        """
        Result:
        [
            <Festo.AST.Testrunner.Interfaces.Entities.Device object at 0x00000226F2BFA000>, 
            <Festo.AST.Testrunner.Interfaces.Entities.Device object at 0x00000226F2C08240>, 
            <Festo.AST.Testrunner.Interfaces.Entities.Device object at 0x00000226F2DC7FC0>
        ]
        """
        # 3
        devices_in_the_topology_python_dict_with_data = {
            device.DeviceId: {
                'ip_address': device.IpAddress,
                'device_type': device.DeviceType,
            }
            for device in devices_in_the_topology_python_list_with_dll_objects
        }
        """
        Result:
        {
            '1': {
                'device_type': 'CMMT-AS-MP', 
                'ip_address': '192.168.2.51'
            }, 
            '2': {
                'device_type': 'CMMT-AS-MP', 
                'ip_address': '192.168.2.52'
            }, 
            '3': {
                'device_type': 'CMMT-ST-MP', 
                'ip_address': '192.168.2.53'
            }
        }
        """

        # 4
        new_project = Project(
            project_name=project_name,
            project_path=project_path,
            git_hash='123123123',       # ToDo: changed it for testing
            topology_type=topology_type,
        )

        # 5
        # ToDo: problem here
        for device_id, device_data in devices_in_the_topology_python_dict_with_data.items():
            if EntityToDbObjectTranslator._check_if_device_is_in_the_db(device_id):
                try:
                    device = Device.objects.get(pk=device_id)
                except Exception as e:
                    print(f"Error getting device from the database: {e}")

                try:
                    print(new_project.devices_in_the_topology.all())
                except Exception as e:
                    print(f"Error getting devices from the project: {e}")

                try:
                    new_project.devices_in_the_topology.add(device)
                except Exception as e:
                    print(f"Error adding device to project: {e}")
            else:
                new_device = Device(
                    ip_address=device_data['ip_address'],
                    device_type=device_data['device_type'],
                )
                new_device.full_clean()
                new_device.save()
                new_project.devices_in_the_topology.add(new_device)

        # 6
        new_project.full_clean()
        new_project.save()        # save is working

        return new_project
