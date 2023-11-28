from rest_framework.decorators import api_view

from core.serializers import PyTerminalSerializer
from core.view_templates import ViewTemplates
from vm_server.py_terminals.models import PyTerminal


@api_view(['GET'])
def get_pyterminals_list(request):
    """
    It is an API view that returns a list of all pyterminals by using the list_view_template static method
    @param request:
    @return: a response with the list of all pyterminals
    """
    return ViewTemplates.list_view_template(PyTerminal, PyTerminalSerializer)


@api_view(['POST'])
def add_pyterminal(request):
    """
    It is an API view that creates a new pyterminal by using the create_view_template static method
    @param request:
    @return: a response with the created pyterminal
    """
    return ViewTemplates.create_view_template(PyTerminalSerializer, request)


@api_view(['GET'])
def show_pyterminal(request, identifier):
    """
    It is an API view that returns a pyterminal by using the show_view_template static method
    @param request:
    @param identifier:
    @return: a response with the pyterminal
    """
    return ViewTemplates.show_view_template(PyTerminal, PyTerminalSerializer, identifier, 'terminal_name')


@api_view(['PUT', 'PATCH'])
def edit_pyterminal(request, identifier):
    """
    It is an API view that edits a pyterminal by using the edit_view_template static method
    @param request:
    @param identifier:
    @return: a response with the edited pyterminal
    """
    return ViewTemplates.edit_view_template(PyTerminal, PyTerminalSerializer, identifier, 'terminal_name', request)


@api_view(['DELETE'])
def delete_pyterminal(request, identifier):
    """
    It is an API view that deletes a pyterminal by using the delete_view_template static method
    @param request:
    @param identifier:
    @return: a response with the deleted pyterminal
    """
    return ViewTemplates.delete_view_template(PyTerminal, identifier, 'terminal_name')
