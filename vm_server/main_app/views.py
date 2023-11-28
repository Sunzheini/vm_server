import subprocess

from rest_framework import status
from rest_framework.views import APIView

from core.view_templates import *
from vm_server.user_management.models import User


# ToDo: all, except the Login logic should be deleted from here after development is finished as it serves only for information purposes


def custom_function():
    print("Hello from custom function")

    script_path = r'C:\Appl\Projects\Python\hello_world.py'

    try:
        result = subprocess.run(["python", script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            output = result.stdout
        else:
            output = f"Script returned an error (exit code {result.returncode}):\n{result.stderr}"
    except Exception as e:
        output = f"Error: {str(e)}"

    return output


# add and edit (POST/PUT, in postman: body --> raw --> JSON) like this:
"""
{
"username":"Daniel Zorov",
"password":"1",
"is_admin": false
}
"""

# call_command('my_vb_controller')
# call_command('close_vb_controller')


def _token_generator(username, password):
    token = username + password
    return token


class LoginView(APIView):
    @staticmethod
    def post(request):
        username = request.data.get('username')
        password = request.data.get('password')

        all_users = User.objects.all()
        for user in all_users:
            if user.username == username and user.password == password:
                # generate an unique token for the user
                token = _token_generator(username, password)

                return Response({'token': token, 'username': user.username, 'id': user.id, 'is_admin': user.is_admin})
        return Response({'error': 'Wrong Credentials'}, status=status.HTTP_400_BAD_REQUEST)
