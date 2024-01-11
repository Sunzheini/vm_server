import requests
import json


class ServerCommunicator:
    """
    This class is used to send commands to the server,
    which is located on the virtual machine.
    """
    def __init__(self, server_url):
        self.url = server_url
        self.headers = {'content-type': 'application/json'}
        self.data = {'command': None}

    def send_command_to_server(self, command):
        """
        Sends a command to the server
        @param command: the command to be sent
        @return: the response from the server
        """
        try:
            self.data['command'] = command
            response = requests.post(self.url, data=json.dumps(self.data), headers=self.headers)

            if response.status_code == 200:
                # return response.json()
                return "Success"
            else:
                return response.status_code

        except Exception as e:
            return f"Exception: {e}"
