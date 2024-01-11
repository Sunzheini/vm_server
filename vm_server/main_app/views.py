from rest_framework import status
from rest_framework.views import APIView
from core.view_templates import *
from vm_server.user_management.models import User


def _token_generator(username, password):
    token = username + password
    return token


class LoginView(APIView):
    """
    A view for the login logic
    """
    @staticmethod
    def post(request):
        """
        A view overwriting the post view and adding the login logic
        @param request:
        @return: returns a token if the user is found, else an error
        """
        username = request.data.get('username')
        password = request.data.get('password')

        all_users = User.objects.all()
        for user in all_users:
            if user.username == username and user.password == password:
                # generate an unique token for the user
                token = _token_generator(username, password)

                return Response({'token': token, 'username': user.username, 'id': user.id, 'is_admin': user.is_admin})
        return Response({'error': 'Wrong Credentials'}, status=status.HTTP_400_BAD_REQUEST)
