import requests
import json


class ServerCommunicator:
    def __init__(self, server_url):
        self.url = server_url
        self.headers = {'content-type': 'application/json'}
        self.data = {'command': None}

    def send_command_to_server(self, command):
        self.data['command'] = command
        response = requests.post(self.url, data=json.dumps(self.data), headers=self.headers)
        return response.json()
