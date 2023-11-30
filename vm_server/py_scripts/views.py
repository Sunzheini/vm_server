from rest_framework.decorators import api_view

from core.serializers import PyScriptSerializer
from core.view_templates import ViewTemplates
from vm_server.py_scripts.models import PyScript


@api_view(['GET'])
def get_py_scripts_list(request):
    """
    It is an API view that returns a list of all py_scripts by using the list_view_template static method
    @param request:
    @return: a response with the list of all py_scripts
    """
    return ViewTemplates.list_view_template(PyScript, PyScriptSerializer)


@api_view(['POST'])
def add_py_script(request):
    """
    It is an API view that creates a new py_script by using the create_view_template static method
    @param request:
    @return: a response with the created py_script
    """
    return ViewTemplates.create_view_template(PyScriptSerializer, request)


@api_view(['GET'])
def show_py_script(request, identifier):
    """
    It is an API view that returns a py_script by using the show_view_template static method
    @param request:
    @param identifier:
    @return: a response with the py_script
    """
    return ViewTemplates.show_view_template(PyScript, PyScriptSerializer, identifier, 'script_name')


@api_view(['PUT', 'PATCH'])
def edit_py_script(request, identifier):
    """
    It is an API view that edits a py_script by using the edit_view_template static method
    @param request:
    @param identifier:
    @return: a response with the edited py_script
    """
    return ViewTemplates.edit_view_template(PyScript, PyScriptSerializer, identifier, 'script_name', request)


@api_view(['DELETE'])
def delete_py_script(request, identifier):
    """
    It is an API view that deletes a py_script by using the delete_view_template static method
    @param request:
    @param identifier:
    @return: a response with the deleted py_script
    """
    return ViewTemplates.delete_view_template(PyScript, identifier, 'script_name')
