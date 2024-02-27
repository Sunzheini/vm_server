from vm_server.virtual_machines.models import Project


class EntityToDbObjectTranslator:
    """
    This class is responsible for creating a database object from an entity from the .NET DLLs.
    """

    @staticmethod
    def create_db_object_from_project_entity(dll_runner, project_entity):
        project_name, project_path, git_hash, topology_type = (
            project_entity.ProjectName,
            project_entity.ProjectPath,
            project_entity.GitHash,
            project_entity.TopologyType,
        )

        devices_in_the_topology_python_list_with_dll_objects = dll_runner.translate_dotnet_generic_list_to_python_list(
            project_entity.ListOfDevicesInTheTopology,
        )
        """
        [
            <Festo.AST.Testrunner.Interfaces.Entities.Device object at 0x00000226F2BFA000>, 
            <Festo.AST.Testrunner.Interfaces.Entities.Device object at 0x00000226F2C08240>, 
            <Festo.AST.Testrunner.Interfaces.Entities.Device object at 0x00000226F2DC7FC0>
        ]
        """
        devices_in_the_topology_python_dict_with_data = {
            device.DeviceId: {
                'ip_address': device.IpAddress,
                'device_type': device.DeviceType,
            }
            for device in devices_in_the_topology_python_list_with_dll_objects
        }
        """
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

        new_project = Project(
            project_name=project_name,
            project_path=project_path,
            git_hash=git_hash,
            topology_type=topology_type,
        )
        # ToDo: what about the devices -> add also the devices to the object before sending it for saving

        return new_project
