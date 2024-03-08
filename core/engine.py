from time import sleep

import requests

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
        @param serializer: The serializer for the model, containing the data to update the object
        """
        # these are the 2 states of the object
        old_state = item

        # use the 2 states to evaluate the need of other actions
        if model.__name__ == 'VM':
            message_update = Engine.vm_decide_actions_based_on_changes(old_state, serializer)
        elif model.__name__ == 'PyScript':
            message_update = Engine.pyscript_decide_actions_based_on_changes(old_state, serializer)

    @staticmethod
    def save_the_serializer(serializer, message_update):
        """
        Saves the object, based on the serializer's data
        @param serializer: The serializer for the model
        @param message_update: The message to be updated
        """
        new_object = serializer.save()
        new_object.update_status(message_update)
        new_object.save()

    @staticmethod
    def pyscript_decide_actions_based_on_changes(old_state_object, serializer):
        """
        Evaluates the need of other actions, based on the object's fields
        When calling Engine.PYSCRIPT_RUNNER.run_script, the script_name is passed as an argument
        and looks like `uploads/hello_world.py`.
        @param old_state_object: The saved state of the object in the db, i.e. TwinCAT,
        if called directly will display the object's name
        @param serializer: The serializer for the model with the data to update the object,
        contains only the fields that have changed!
        @return: String with the action that needs to be performed
        """
        new_state_ordered_dict = serializer.validated_data  # OrderedDict([('script_is_executed', True)])
        key = list(new_state_ordered_dict.keys())[0]
        value = new_state_ordered_dict[key]

        if key == 'script_name':
            if value != old_state_object.script_name:
                try:
                    result_string = f'Changed script to: {value}'
                    Engine.save_the_serializer(serializer, result_string)
                    return result_string
                except Exception as e:
                    old_state_object.update_status(f'Exception: {e}')
                    old_state_object.save()
                    return f'Exception: {e}'

        elif key == 'script_is_executed':
            try:
                result = Engine.PYSCRIPT_RUNNER.run_script(old_state_object.script_file)
                Engine.save_the_serializer(serializer, result)
                return result
            except Exception as e:
                old_state_object.update_status(f'Exception: {e}')
                old_state_object.save()
                return f'Exception: {e}'

        else:
            return 'Updated status'

    @staticmethod
    def vm_decide_actions_based_on_changes(old_state_object, serializer):
        """
        Evaluates the need of other actions, based on the object's fields
        @param old_state_object: the saved state of the object in the db, i.e. TwinCAT,
        if called directly will display the object's name
        @param serializer: The serializer for the model with the data to update the object,
        contains only the fields that have changed!
        i.e. `VMSerializer(<VM: TwinCAT>)`
        @return: String with the action that needs to be performed
        """
        new_state_ordered_dict = serializer.validated_data  # OrderedDict([('machine_is_started', True)])
        key = list(new_state_ordered_dict.keys())[0]        # 'machine_is_started'
        value = new_state_ordered_dict[key]                 # True
        """
        Now we check the key and value and decide what to do. Each key corresponds to a
        specific button on the frontend.
        """

        # key: vm_name
        # -----------------------------------------------------
        if key == 'vm_name':
            if value != old_state_object.vm_name:
                try:
                    result_string = f"Changed vm_name to: {value}"
                    Engine.save_the_serializer(serializer, result_string)
                except Exception as e:
                    old_state_object.update_status(f'Exception: {e}')
                    old_state_object.save()
                    result_string = f'Exception: {e}'
                return result_string

        # key: selected_plc
        # -----------------------------------------------------
        elif key == 'selected_plc':
            if value != old_state_object.selected_plc:
                try:
                    result_string = f"Changed selected_plc to: {value}"
                    Engine.save_the_serializer(serializer, result_string)
                except Exception as e:
                    old_state_object.update_status(f'Exception: {e}')
                    old_state_object.save()
                    result_string = f'Exception: {e}'
                return result_string

        # key: sequence_is_initiated
        # -----------------------------------------------------
        elif key == 'sequence_is_initiated':
            Engine.SELECTED_VM_NAME = old_state_object.vm_name

            try:
                Engine.VB_CONTROLLER.initiate_machine(old_state_object.vm_name)
                sleep(5)
                response = Engine.COMMUNICATOR.send_command_to_server('1')
                sleep(10)
                response = Engine.COMMUNICATOR.send_command_to_server('5')
                sleep(10)
                response = Engine.COMMUNICATOR.send_command_to_server('6')
                sleep(10)
                response = Engine.COMMUNICATOR.send_command_to_server('2')
                sleep(5)
                Engine.VB_CONTROLLER.power_down(old_state_object.vm_name)
                result_string = f'VM sequence finished: {response}'

                Engine.save_the_serializer(serializer, result_string)
                return result_string

            except Exception as e:
                old_state_object.update_status(f'Exception: {e}')
                old_state_object.save()
                result_string = f'Exception: {e}'
                return result_string

        # key: machine_is_started
        # -----------------------------------------------------
        elif key == 'machine_is_started':
            if value != old_state_object.machine_is_started:
                # assign the selected vm name to the class variable
                Engine.SELECTED_VM_NAME = old_state_object.vm_name

                # if 'machine_is_started' is True
                if value:
                    try:
                        Engine.VB_CONTROLLER.initiate_machine(old_state_object.vm_name)
                        sleep(5)
                        response = Engine.COMMUNICATOR.send_command_to_server('1')
                        result_string = f'VM process started: {response}'

                        Engine.save_the_serializer(serializer, result_string)
                        return result_string

                    except Exception as e:
                        old_state_object.update_status(f'Exception: {e}')
                        old_state_object.save()
                        result_string = f'Exception: {e}'
                        return result_string

                # if 'machine_is_started' is False
                else:
                    try:
                        response = Engine.COMMUNICATOR.send_command_to_server('2')
                        sleep(5)
                        Engine.VB_CONTROLLER.power_down(old_state_object.vm_name)
                        result_string = f'VM process stopped: {response}'

                        Engine.save_the_serializer(serializer, result_string)
                        return result_string

                    except Exception as e:
                        old_state_object.update_status(f'Exception: {e}')
                        old_state_object.save()
                        result_string = f'Exception: {e}'
                        return result_string

        # key: path_to_selected_program
        # -----------------------------------------------------
        elif key == 'path_to_selected_program':
            if value != old_state_object.path_to_selected_program:
                try:
                    result_string = f'Changed path to: {value}'
                    Engine.save_the_serializer(serializer, result_string)
                    return result_string
                except Exception as e:
                    old_state_object.update_status(f'Exception: {e}')
                    old_state_object.save()
                    return f'Exception: {e}'
            else:
                result_string = 'It is the same path'
                return result_string

        # key: program_is_open
        # -----------------------------------------------------
        elif key == 'program_is_open':
            if value != old_state_object.program_is_open:
                if value:
                    try:
                        response = Engine.COMMUNICATOR.send_command_to_server('3')
                        result_string = f'Opened program: {response}'

                        Engine.save_the_serializer(serializer, result_string)
                        return result_string
                    except Exception as e:
                        old_state_object.update_status(f'Exception: {e}')
                        old_state_object.save()
                        return f'Exception: {e}'
                else:
                    try:
                        response = Engine.COMMUNICATOR.send_command_to_server('4')
                        result_string = f'Closed program: {response}'

                        Engine.save_the_serializer(serializer, result_string)
                        return result_string
                    except Exception as e:
                        old_state_object.update_status(f'Exception: {e}')
                        old_state_object.save()
                        return f'Exception: {e}'

        # key: program_is_compiled
        # -----------------------------------------------------
        elif key == 'program_is_compiled':
            try:
                response = Engine.COMMUNICATOR.send_command_to_server('5')
                result_string = f'Compiled program: {response}'

                Engine.save_the_serializer(serializer, result_string)
                return result_string
            except Exception as e:
                old_state_object.update_status(f'Exception: {e}')
                old_state_object.save()
                return f'Exception: {e}'

        # key: program_is_downloaded
        # -----------------------------------------------------
        elif key == 'program_is_downloaded':
            try:
                response = Engine.COMMUNICATOR.send_command_to_server('6')
                result_string = f'Downloaded program: {response}'

                Engine.save_the_serializer(serializer, result_string)
                return result_string
            except Exception as e:
                old_state_object.update_status(f'Exception: {e}')
                old_state_object.save()
                return f'Exception: {e}'

        # key: connection_is_online
        # -----------------------------------------------------
        elif key == 'connection_is_online':
            if value != old_state_object.connection_is_online:
                if value:
                    try:
                        response = Engine.COMMUNICATOR.send_command_to_server('7')
                        result_string = f'Connected to PLC: {response}'

                        Engine.save_the_serializer(serializer, result_string)
                        return result_string
                    except Exception as e:
                        old_state_object.update_status(f'Exception: {e}')
                        old_state_object.save()
                        return f'Exception: {e}'
                else:
                    try:
                        response = Engine.COMMUNICATOR.send_command_to_server('8')
                        result_string = f'Disconnected from PLC: {response}'

                        Engine.save_the_serializer(serializer, result_string)
                        return result_string
                    except Exception as e:
                        old_state_object.update_status(f'Exception: {e}')
                        old_state_object.save()
                        return f'Exception: {e}'

        # key: plc_is_running
        # -----------------------------------------------------
        elif key == 'plc_is_running':
            if value != old_state_object.plc_is_running:
                if value:
                    try:
                        response = Engine.COMMUNICATOR.send_command_to_server('9')
                        result_string = f'Started PLC: {response}'

                        Engine.save_the_serializer(serializer, result_string)
                        return result_string
                    except Exception as e:
                        old_state_object.update_status(f'Exception: {e}')
                        old_state_object.save()
                        return f'Exception: {e}'
                else:
                    try:
                        response = Engine.COMMUNICATOR.send_command_to_server('10')
                        result_string = f'Stopped PLC: {response}'

                        Engine.save_the_serializer(serializer, result_string)
                        return result_string
                    except Exception as e:
                        old_state_object.update_status(f'Exception: {e}')
                        old_state_object.save()
                        return f'Exception: {e}'

        # key: enabled
        # -----------------------------------------------------
        elif key == 'enabled':
            if value != old_state_object.enabled:
                if value:
                    try:
                        response = Engine.COMMUNICATOR.send_command_to_server('11')
                        result_string = f'Enabled: {response}'

                        Engine.save_the_serializer(serializer, result_string)
                        return result_string
                    except Exception as e:
                        old_state_object.update_status(f'Exception: {e}')
                        old_state_object.save()
                        return f'Exception: {e}'
                else:
                    try:
                        response = Engine.COMMUNICATOR.send_command_to_server('12')
                        result_string = f'Disabled: {response}'

                        Engine.save_the_serializer(serializer, result_string)
                        return result_string
                    except Exception as e:
                        old_state_object.update_status(f'Exception: {e}')
                        old_state_object.save()
                        return f'Exception: {e}'

        else:
            return 'Updated status'
