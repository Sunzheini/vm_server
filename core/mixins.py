from core.db_object_to_entity_translator import DbObjectToEntityTranslator
from core.entity_to_db_object_translator import EntityToDbObjectTranslator
from vm_server.virtual_machines.models import Plc, Project


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
        @param request_attributes_list: list of strings
        @param response_object: object of type G01_ResponsePlcMetaData
        @param dll_runner: object
        """
        plc_id = request_attributes_list[0]                                                                         # 1

        latest_project = RequestAndResponsePlcMetaDataMixin.find_project_based_on_plc_id(plc_id)                    # 2
        new_project = DbObjectToEntityTranslator.create_project_entity_from_db_object(dll_runner, latest_project)   # 3
        response_object.Project = new_project                                                                       # 4

    @staticmethod
    def find_project_based_on_plc_id(plc_id):
        """
        Find the latest project loaded on the PLC
        Result: object of Project class
        @param plc_id: string
        @return: object of Project class
        """
        try:
            plc = Plc.objects.get(pk=plc_id)
            if plc.loaded_project:
                latest_project = plc.loaded_project
                return latest_project
            else:
                return None
        except Plc.DoesNotExist:
            return None


class RequestAndResponsePlcConfigureMixin:
    """
    A mixin class that contains needed metadata for the connection with the relevant dll classes.
    """
    _REQUEST_CLASS = 'G02_RequestPlcConfigure'
    _REQUEST_ATTRIBUTES = ['IdOfPlcToRequest', 'Project']
    _RESPONSE_CLASS = 'G03_ResponsePlcConfigure'

    @staticmethod
    def handle_plc_configure(request_attributes_list, response_object, dll_runner):
        plc_id = request_attributes_list[0]
        prj_to_be_loaded = request_attributes_list[1]

        # check if git hash exists in the database, if not, create a new project object and save it in the database
        if RequestAndResponsePlcConfigureMixin.check_if_git_hash_exists(prj_to_be_loaded.GitHash):
            db_project_object = EntityToDbObjectTranslator.create_db_object_from_project_entity(
                dll_runner,
                prj_to_be_loaded
            )
            print(db_project_object)
            """
            Result:
            Project Id: 3, Name: Project1, Path: path..., Git hash: 123123123, Topology type: 3, Devices: []
            """

        # ToDo: continue from here.

        # ToDo: After 68 is working add `not`

        # else, get the project object from the database
        else:
            db_project_object = Project.objects.get(git_hash=prj_to_be_loaded.GitHash)

    @staticmethod
    def check_if_git_hash_exists(git_hash):
        try:
            Project.objects.get(git_hash=git_hash)
            return True
        except Project.DoesNotExist:
            return False
