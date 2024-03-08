from core.db_search_tools import find_project_based_on_plc_id, check_if_git_hash_exists, find_plc_based_on_id
from core.db_object_to_entity_translator import DbObjectToEntityTranslator
from core.engine import Engine
from core.entity_to_db_object_translator import EntityToDbObjectTranslator
from core.serializers import VMSerializer
from vm_server.virtual_machines.models import Project, VM


class RequestAndResponsePlcMetaDataMixin:
    """
    A mixin class that contains needed metadata for the connection with the relevant dll classes.
    """
    _REQUEST_CLASS = 'G00_RequestPlcMetaData'
    _REQUEST_ATTRIBUTES = ['IdOfPlcToRequest', ]
    _RESPONSE_CLASS = 'G01_ResponsePlcMetaData'

    @staticmethod
    def handle_info_exchange(request_attributes_list, response_object, dll_runner):
        """
        1. Store the value of the request attribute in a variable
        Result: string
        2. Find the latest project loaded on the PLC
        Result: object of Project class
        3. Create a new project object using the EntityFactory class.
        Result: object of Project class
        4. Set the Project attribute of the G01_ResponsePlcMetaData object to the new project object
        Result: object of Project class
        @rtype: object
        @param request_attributes_list: list of strings
        @param response_object: object of type G01_ResponsePlcMetaData
        @param dll_runner: object
        """
        plc_id = request_attributes_list[0]                                                                         # 1

        latest_project_attached_to_plc_db_object = find_project_based_on_plc_id(plc_id)     # 2
        project_to_be_attached_to_the_response = DbObjectToEntityTranslator.create_project_entity_from_db_object(
            dll_runner, latest_project_attached_to_plc_db_object
        )                                                                                   # 3
        response_object.Project = project_to_be_attached_to_the_response                    # 4


class RequestAndResponsePlcConfigureMixin:
    """
    A mixin class that contains needed metadata for the connection with the relevant dll classes.
    """
    _REQUEST_CLASS = 'G02_RequestPlcConfigure'
    _REQUEST_ATTRIBUTES = ['IdOfPlcToRequest', 'Project']
    _RESPONSE_CLASS = 'G03_ResponsePlcConfigure'

    @staticmethod
    def handle_plc_configure(request_attributes_list, response_object, dll_runner):
        """
        1. Store the value of the request attribute in a variable
        2. Check if the git hash exists in the db and if not, create a new project object and save it in db
            Result:
            Project Id: 3, Name: Project1, Path: path..., Git hash: 123123123, Topology type: 3, Devices: []
        @param request_attributes_list: list of strings
        @param response_object: object of type G01_ResponsePlcMetaData
        @param dll_runner: object
        """
        plc_id = request_attributes_list[0]
        prj_to_be_loaded = request_attributes_list[1]

        # If git hash does not exist in the db, create a new project object and save it in db
        if not check_if_git_hash_exists(prj_to_be_loaded.GitHash):
            db_project_object = EntityToDbObjectTranslator.create_db_object_from_project_entity(
                dll_runner,
                prj_to_be_loaded
            )
        else:
            db_project_object = Project.objects.get(git_hash=prj_to_be_loaded.GitHash)

        # Set the loaded project to the PLC
        plc = find_plc_based_on_id(plc_id)
        plc.loaded_project = db_project_object
        plc.save()

        plc_to_be_attached_to_response = DbObjectToEntityTranslator.create_plc_entity_from_db_object(
            dll_runner, plc
        )

        response_object.Plc = plc_to_be_attached_to_response
        response_object.Project = prj_to_be_loaded
        response_object.LogData = f"Project {prj_to_be_loaded.ProjectName} loaded on PLC {plc_id}"


class RequestAndResponseStartVmProcessMixin:
    """
    A mixin class that contains needed metadata for the connection with the relevant dll classes.
    """
    _REQUEST_CLASS = 'G04_RequestStartVmProcess'
    _REQUEST_ATTRIBUTES = ['IdOfPlcToRequest', ]
    _RESPONSE_CLASS = 'G05_ResponseStartVmProcess'

    @staticmethod
    def handle_start_vm_process(request_attributes_list, response_object, dll_runner):
        """
        1. Store the value of the request attribute in a variable
        2. Find the PLC based on the ID
        3. Get the VM type from the PLC
        4. Call the Engine class to decide the actions based on the changes in the VM
        @param request_attributes_list: list of strings
        @param response_object: object of type G01_ResponsePlcMetaData
        @param dll_runner: object of type DllRunner
        """
        plc_id = request_attributes_list[0]                                                                         # 1
        plc = find_plc_based_on_id(plc_id)
        vm_type = plc.vendor_name
        vm = VM.objects.get(vm_type=vm_type)

        data_for_serializer = {'sequence_is_initiated': False}
        serializer = VMSerializer(vm, data_for_serializer, partial=True)
        if serializer.is_valid():
            result = Engine.vm_decide_actions_based_on_changes(
                vm,
                serializer,
            )
            response_object.LogData = result
