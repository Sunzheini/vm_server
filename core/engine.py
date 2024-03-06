from controllers.pyscript_runner import PyScriptRunner
from controllers.server_communicator import ServerCommunicator
from controllers.vb_controller import VBController
from vm_server.settings import url_of_server_on_vm


class Engine:
    """
    The Engine class is responsible for the logic of the application. Connects the requests from the client
    with the specific logic for the virtual machine control and/or python script execution.
    """
    # Keep the selected vm name in a class variable
    SELECTED_VM_NAME = None

    # Initiate the controllers
    VB_CONTROLLER = VBController()
    COMMUNICATOR = ServerCommunicator(url_of_server_on_vm)
    PYSCRIPT_RUNNER = PyScriptRunner()

    # Action Distribution based on received command from the client
    @staticmethod
    def update_the_model(model, item, serializer):
        """
        Updates the model, based on the serializer's data
        @param model: The model class
        @param item: The corresponding object from the db
        @param serializer: The serializer
        """
        # these are the 2 states of the object
        old_state = item
        new_state = serializer.validated_data
        message_update = ''

        # use the 2 states to evaluate the need of other actions
        if model.__name__ == 'VM':
            message_update = Engine.vm_decide_actions_based_on_changes(old_state, new_state)
        elif model.__name__ == 'PyScript':
            message_update = Engine.pyscript_decide_actions_based_on_changes(old_state, new_state)

        # continue with the update
        new_object = serializer.save()
        new_object.update_status(message_update)
        new_object.save()

    @staticmethod
    def pyscript_decide_actions_based_on_changes(old_state_object, new_state_ordered_dict):
        """
        Evaluates the need of other actions, based on the object's fields
        When calling Engine.PYSCRIPT_RUNNER.run_script, the script_name is passed as an argument
        and looks like `uploads/hello_world.py`.
        @param new_state_ordered_dict:
        @param old_state_object: The saved state of the object in the db, i.e. TwinCAT,
        if called directly will display the object's name
        @param new_state_ordered_dict: an ordered dict with the object's fields and values,
        contains only the fields that have changed!
        @return: String with the action that needs to be performed
        """
        key = list(new_state_ordered_dict.keys())[0]
        value = new_state_ordered_dict[key]

        if key == 'script_name':
            if value != old_state_object.script_name:
                return f'Changed script_name to: {value}'

        elif key == 'script_is_executed':
            result = Engine.PYSCRIPT_RUNNER.run_script(old_state_object.script_file)
            return result

        else:
            return 'Updated status'

    @staticmethod
    def vm_decide_actions_based_on_changes(old_state_object, new_state_ordered_dict):
        """
        Evaluates the need of other actions, based on the object's fields
        @param old_state_object: the saved state of the object in the db, i.e. TwinCAT,
        if called directly will display the object's name
        @param new_state_ordered_dict: an ordered dict with the object's fields and values,
        contains only the fields that have changed!
        I.e. `OrderedDict([('connection_is_online', True)])`
        @return: String with the action that needs to be performed
        """
        key = list(new_state_ordered_dict.keys())[0]
        value = new_state_ordered_dict[key]
        """
        Now we check the key and value and decide what to do. Each key corresponds to a
        specific button on the frontend.
        """

        # key: vm_name
        # -----------------------------------------------------
        if key == 'vm_name':
            if value != old_state_object.vm_name:
                return f'Changed vm_name to: {value}'

        # key: machine_is_started
        # -----------------------------------------------------
        elif key == 'machine_is_started':
            if value != old_state_object.machine_is_started:
                # assign the selected vm name to the class variable
                Engine.SELECTED_VM_NAME = old_state_object.vm_name

                if value:
                    try:
                        # result_string = Engine.VB_CONTROLLER.initiate_machine(Engine.SELECTED_VM_NAME)
                        result_string = 'Success'
                        if result_string != 'Success':
                            return result_string
                        return 'Started machine'
                    except Exception as e:
                        return f'Exception: {e}'
                else:
                    try:
                        # result_string = Engine.VB_CONTROLLER.power_down(Engine.SELECTED_VM_NAME)
                        result_string = 'Success'
                        if result_string != 'Success':
                            return result_string
                        return 'Stopped machine'
                    except Exception as e:
                        return f'Exception: {e}'

        # key: path_to_selected_program
        # -----------------------------------------------------
        elif key == 'path_to_selected_program':
            if value != old_state_object.path_to_selected_program:
                result = Engine.COMMUNICATOR.send_command_to_server(f'change program path to: {value}')
                if result != 'Success':
                    return f'Changed path to: {value}'
                else:
                    return result

        # key: program_is_open
        # -----------------------------------------------------
        elif key == 'program_is_open':
            if value != old_state_object.program_is_open:
                if value:
                    result = Engine.COMMUNICATOR.send_command_to_server('open program')
                    if result != 'Success':
                        return 'Opened program'
                    else:
                        return result
                else:
                    result = Engine.COMMUNICATOR.send_command_to_server('close program')
                    if result != 'Success':
                        return 'Closed program'
                    else:
                        return result

        # key: program_is_compiled
        # -----------------------------------------------------
        elif key == 'program_is_compiled':
            result = Engine.COMMUNICATOR.send_command_to_server('compile')
            if result != 'Success':
                return 'Compiled program'
            else:
                return result

        # key: program_is_downloaded
        # -----------------------------------------------------
        elif key == 'program_is_downloaded':
            result = Engine.COMMUNICATOR.send_command_to_server('download')
            if result != 'Success':
                return 'Downloaded program'
            else:
                return result

        # key: connection_is_online
        # -----------------------------------------------------
        elif key == 'connection_is_online':
            if value != old_state_object.connection_is_online:
                if value:
                    result = Engine.COMMUNICATOR.send_command_to_server('connect')
                    if result != 'Success':
                        return 'Connected to PLC'
                    else:
                        return result
                else:
                    result = Engine.COMMUNICATOR.send_command_to_server('disconnect')
                    if result != 'Success':
                        return 'Disconnected from PLC'
                    else:
                        return result

        # key: plc_is_running
        # -----------------------------------------------------
        elif key == 'plc_is_running':
            if value != old_state_object.plc_is_running:
                if value:
                    result = Engine.COMMUNICATOR.send_command_to_server('start_plc')
                    if result != 'Success':
                        return 'Started PLC'
                    else:
                        return result
                else:
                    result = Engine.COMMUNICATOR.send_command_to_server('stop_plc')
                    if result != 'Success':
                        return 'Stopped PLC'
                    else:
                        return result

        # key: enabled
        # -----------------------------------------------------
        elif key == 'enabled':
            if value != old_state_object.enabled:
                if value:
                    result = Engine.COMMUNICATOR.send_command_to_server('enable')
                    if result != 'Success':
                        return 'Enabled'
                    else:
                        return result
                else:
                    result = Engine.COMMUNICATOR.send_command_to_server('disable')
                    if result != 'Success':
                        return 'Disabled'
                    else:
                        return result
        else:
            return 'Updated status'
