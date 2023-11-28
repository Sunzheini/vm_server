from rest_framework.decorators import api_view

from core.serializers import UserSerializer
from core.view_templates import ViewTemplates
from vm_server.user_management.models import User


@api_view(['GET'])
def get_users_list(request):
    """
    It is an API view that returns a list of all users by using the list_view_template static method
    @param request:
    @return: a response with the list of all users
    """
    result = ViewTemplates.list_view_template(User, UserSerializer)
    return result


@api_view(['POST'])
def add_user(request):
    """
    It is an API view that creates a new user by using the create_view_template static method
    @param request:
    @return: a response with the created user
    """
    return ViewTemplates.create_view_template(UserSerializer, request)


@api_view(['GET'])
def show_user(request, identifier):
    """
    It is an API view that returns a user by using the show_view_template static method
    @param request:
    @param identifier:
    @return: a response with the user
    """
    return ViewTemplates.show_view_template(User, UserSerializer, identifier, 'username')


@api_view(['PUT', 'PATCH'])
def edit_user(request, identifier):
    """
    It is an API view that edits a user by using the edit_view_template static method
    @param request:
    @param identifier:
    @return: a response with the edited user
    """
    return ViewTemplates.edit_view_template(User, UserSerializer, identifier, 'username', request)


@api_view(['DELETE'])
def delete_user(request, identifier):
    """
    It is an API view that deletes a user by using the delete_view_template static method
    @param request:
    @param identifier:
    @return: a response with the deleted user
    """
    return ViewTemplates.delete_view_template(User, identifier, 'username')
