import json
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response

from constants.constants import core_dll_path, core_dll_name, core_dll_imports, \
framework_dll_path, framework_dll_name, framework_dll_imports
from core.dll_runner import DllRunner
from core.db_object_to_entity_translator import DbObjectToEntityTranslator
from core.mixins import RequestAndResponsePlcMetaDataMixin, RequestAndResponsePlcConfigureMixin
from core.serializers import VMSerializer, VMTypeSerializer
from core.view_templates import ViewTemplates
from vm_server.virtual_machines.models import VM, vm_type_choices


"""
Import the DLL runner and initialize it. The DLL runner is a class that is used to run .NET DLLs from Python. It is
initialized with the path to the DLL, the name of the DLL, and the imports that are needed from the DLL. The imports
are a list of dictionaries, where each dictionary contains the namespace and the classes that are needed from that
namespace. The DLL runner is used to create instances of the classes from the DLL and to call their methods. The
DLL runner is used to call the methods from the DLL in the API views.

Choose either framework or core, based on parameters.
"""
dll_runner = DllRunner(core_dll_path, core_dll_name, core_dll_imports)
# dll_runner = DllRunner(framework_dll_path, framework_dll_name, framework_dll_imports)


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
        """
        It is an API view that returns a list of all vm types. Needed to get the vm types for the list of choices
        when creating a new vm
        @param request: a request from the frontend requesting the vm types
        @param args: available arguments
        @param kwargs: available keyword arguments
        @return: a response with the list of all vm types
        """
        # Assuming VM types are defined in vm_type_choices
        vm_types = [{'vm_type': choice[0]} for choice in vm_type_choices]
        serializer = VMTypeSerializer(vm_types, many=True)
        return Response(serializer.data)


class BaseDllCommunicationClassView(APIView):
    """
    This class is an API view that receives a POST request and returns a response, using the DLL
    runner as an example. In the current case it handles the request-plc-meta-data endpoint.
    Receives an id of a PLC, finds the latest project loaded on the PLC and returns it.
    """
    @staticmethod
    def get(request, *args, **kwargs):
        response = {'message': 'Hello, World!'}
        return Response(response, status=status.HTTP_200_OK)

    def _before_custom_post_logic(self, request):
        """
        1. Extract the data from the POST request. In the context of Django, `request.data` is often
        equivalent to the body of the request. However, it's important to note that `request.data` might
        not always be the raw body content. Django parses it into a more accessible format based on the
        content type of the request. For example, if the request is sent with JSON content, `request.data`
        will contain a Python dictionary representing the JSON data. If it's form data, it will be a
        QueryDict object. Result: `{'idOfPlcToRequest': '123'}`

        2. {'idOfPlcToRequest': '123'} is a valid JSON object, but it's represented as a Python dictionary.
        In Python, a JSON object and a dictionary are similar data structures, but they are not the same.
        Therefore, you need to convert the dictionary to a JSON-formatted string using json.dumps()
        before passing it to the method. Result: '{"idOfPlcToRequest": "123"}'

        3. Create an instance of G00_RequestPlcMetaData class and deserialize the JSON string.
        ConvertFromJson is a static method, so it is called on the class. Results:
        - g00_template_object: object of type G00_RequestPlcMetaData
        - deserialized_g00: object
        - id_of_plc_to_request: string: '123'

        4. Create an instance of G01_ResponsePlcMetaData class and set the project attribute
        Result: object of type G01_ResponsePlcMetaData
        @param request: the request object, which contains the json data
        @return: a tuple with the request attribute value and the response object
        """
        request_data = request.data                                                                                 # 1
        request_data_json_string = json.dumps(request_data)                                                         # 2
        request_template_object = eval(f'dll_runner.{self._REQUEST_CLASS}()')                                       # 3
        deserialized_request_template_object = request_template_object.ConvertFromJson(request_data_json_string)

        request_attribute_values_list = []
        for attribute in self._REQUEST_ATTRIBUTES:
            temp = eval(f'deserialized_request_template_object.{attribute}')
            request_attribute_values_list.append(temp)

        response_object = eval(f'dll_runner.{self._RESPONSE_CLASS}()')                                              # 4
        # return request_attribute_value, response_object
        return request_attribute_values_list, response_object

    @staticmethod
    def _after_custom_post_logic(response_object):
        """
        6. Convert the G01_ResponsePlcMetaData object to a JSON string and deserialize it. The
        json.loads() is used to deserialize a JSON string into a Python object.
        Result: JSON string
        7. deserialize a JSON string into a Python object. Result: dictionary
        @param response_object: object of type G01_ResponsePlcMetaData
        @return: a dictionary with the deserialized response
        """
        response = response_object.ConvertToJson()  # 6
        deserialized_response = json.loads(response)
        return deserialized_response


class RequestAndResponsePlcMetaDataClassView(BaseDllCommunicationClassView, RequestAndResponsePlcMetaDataMixin):
    def post(self, request, *args, **kwargs):
        """
        This view receives a POST request and returns a response, using the DLL runner as an example.
        :param request: the request object, which contains the json data
        :return: a response with needed data
        1. Extract the data from the POST request
        2. Use external method to:
        Create a new project object using the EntityFactory class.
        Result: object of Project class
        Set the Project attribute of the G01_ResponsePlcMetaData object to the new project object
        Result: object of Project class
        3. Convert the G01_ResponsePlcMetaData object to a JSON string and deserialize it.
        Result: dictionary
        """
        try:
            request_attributes_list, response_object = self._before_custom_post_logic(request)

            RequestAndResponsePlcMetaDataMixin.handle_info_exchange(
                request_attributes_list,
                response_object,
                dll_runner,
            )

            deserialized_response = self._after_custom_post_logic(response_object)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(deserialized_response, status=status.HTTP_200_OK)


class RequestAndResponsePlcConfigureClassView(BaseDllCommunicationClassView, RequestAndResponsePlcConfigureMixin):
    def post(self, request, *args, **kwargs):
        try:
            request_attributes_list, response_object = self._before_custom_post_logic(request)

            RequestAndResponsePlcConfigureMixin.handle_plc_configure(
                request_attributes_list,
                response_object,
                dll_runner,
            )

            deserialized_response = self._after_custom_post_logic(response_object)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(deserialized_response, status=status.HTTP_200_OK)
