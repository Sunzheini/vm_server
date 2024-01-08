from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response

from core.serializers import VMSerializer, VMTypeSerializer
from core.view_templates import ViewTemplates
from vm_server.virtual_machines.models import VM, vm_type_choices


@api_view(['GET'])
def get_vms_list(request):
    """
    It is an API view that returns a list of all vms by using the list_view_template static method
    @param request:
    @return: a response with the list of all vms
    """
    return ViewTemplates.list_view_template(VM, VMSerializer)


@api_view(['POST'])
def add_vm(request):
    """
    It is an API view that creates a new vm by using the create_view_template static method
    @param request:
    @return: a response with the created vm
    """
    return ViewTemplates.create_view_template(VMSerializer, request)


@api_view(['GET'])
def show_vm(request, identifier):
    """
    It is an API view that returns a vm by using the show_view_template static method
    @param request:
    @param identifier:
    @return: a response with the vm
    """
    return ViewTemplates.show_view_template(VM, VMSerializer, identifier, 'vm_name')


@api_view(['PUT', 'PATCH'])
def edit_vm(request, identifier):
    """
    It is an API view that edits a vm by using the edit_view_template static method
    @param request:
    @param identifier:
    @return: a response with the edited vm
    """
    return ViewTemplates.edit_view_template(VM, VMSerializer, identifier, 'vm_name', request)


@api_view(['DELETE'])
def delete_vm(request, identifier):
    """
    It is an API view that deletes a vm by using the delete_view_template static method
    @param request:
    @param identifier:
    @return: a response with the deleted vm
    """
    return ViewTemplates.delete_view_template(VM, identifier, 'vm_name')


class VMTypeView(APIView):
    def get(self, request, *args, **kwargs):
        # Assuming VM types are defined in vm_type_choices
        vm_types = [{'vm_type': choice[0]} for choice in vm_type_choices]
        serializer = VMTypeSerializer(vm_types, many=True)
        return Response(serializer.data)
