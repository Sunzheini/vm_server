class DbObjectToEntityTranslator:
    """
    This class is responsible for creating an entity from a database object. The `entities`
    are the names of the classes in the dll, which define the structure of the data, i.e. the `Device`
    and the `Plc` class.
    """
    @staticmethod
    def create_project_entity_from_db_object(dll_runner, latest_project):
        """
        Create a new project object using the EntityFactory class.
        1. Get the project name, project path, git hash, and topology type from the latest project
        2. Create new device objects and add them to a list. Create a .NET list of device objects and add the new
        device objects to it
        3. Create a new project object
        @param dll_runner: the object of the DllRunner class
        @param latest_project: the object of the Project class
        @return: object of Project class
        """
        # 1
        project_name, project_path, git_hash, topology_type = (
            latest_project.project_name,
            latest_project.project_path,
            latest_project.git_hash,
            latest_project.topology_type,
        )

        # 2
        devices_list = latest_project.devices_in_the_topology.all()
        new_device_list = []
        [new_device_list.append(dll_runner.Device(str(device.pk), str(device.ip_address), str(device.device_type)))
         for device in devices_list]
        dotnet_device_list = dll_runner.translate_python_list_to_dotnet_generic_list(new_device_list, dll_runner.Device)

        # 3
        new_project = dll_runner.Project(
            project_name,
            project_path,
            git_hash,
            topology_type,
            dotnet_device_list,
        )

        return new_project
