import os
import requests

from controllers.server_communicator_instance import srv_communicator
from controllers.vb_controller_instance import vb_controller


# ToDo: fix engine.py starting from evaluate_need_of_other_actions!
url = 'https://github.com/Sunzheini/zed_hub/blob/main/README.md'


class Engine:
    # ---------------------------------------------------------------
    # URL
    # ---------------------------------------------------------------
    @staticmethod
    def download_text_from_url(address):
        response = requests.get(url)
        response.raise_for_status()
        return response.text

    @staticmethod
    def get_it(address):
        try:
            text_content = Engine.download_text_from_url(url)
            if text_content is not None:
                print("Text content:")
                print(text_content)
        except Exception as e:
            print(f"Error: {e}")

    # ---------------------------------------------------------------
    # Action Distribution
    # ---------------------------------------------------------------
    @staticmethod
    def update_the_model(model, item, serializer):
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
        @param old_state: the saved state of the object in the db, i.e. TwinCAT
        @param new_state: the new state of the object, i.e. React
        @return:
        """
        key = list(new_state_ordered_dict.keys())[0]
        value = new_state_ordered_dict[key]

        if key == 'script_name':
            if value != old_state_object.script_name:
                return f'Changed script_name to: {value}'
        elif key == 'script_is_executed':
            return 'Executed script'
        else:
            return 'Updated status'

    @staticmethod
    def vm_decide_actions_based_on_changes(old_state_object, new_state_ordered_dict):
        """
        Evaluates the need of other actions, based on the object's fields
        @param old_state_object: the saved state of the object in the db, i.e. TwinCAT
        @param new_state_ordered_dict: an ordered dict with the object's fields and values,
        contains only the fields that have changed!
        I.e. `OrderedDict([('connection_is_online', True)])`
        @return:
        """
        key = list(new_state_ordered_dict.keys())[0]
        value = new_state_ordered_dict[key]

        if key == 'vm_name':
            if value != old_state_object.vm_name:
                return f'Changed vm_name to: {value}'
        elif key == 'machine_is_started':
            if value != old_state_object.machine_is_started:
                if value:
                    return 'Started machine'
                else:
                    return 'Stopped machine'
        elif key == 'path_to_selected_program':
            if value != old_state_object.path_to_selected_program:
                return f'Updated path to: {value}'
        elif key == 'program_is_open':
            if value != old_state_object.program_is_open:
                if value:
                    return 'Opened program'
                else:
                    return 'Closed program'
        elif key == 'program_is_compiled':
            return 'Compiled program'
        elif key == 'program_is_downloaded':
            return 'Downloaded program'
        elif key == 'connection_is_online':
            if value != old_state_object.connection_is_online:
                if value:
                    return 'Connected to PLC'
                else:
                    return 'Disconnected from PLC'
        elif key == 'plc_is_running':
            if value != old_state_object.plc_is_running:
                if value:
                    return 'Started PLC'
                else:
                    return 'Stopped PLC'
        elif key == 'enabled':
            if value != old_state_object.enabled:
                if value:
                    return 'Enabled'
                else:
                    return 'Disabled'
        else:
            return 'Updated status'
