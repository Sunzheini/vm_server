import subprocess

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view

from rest_framework import status
from rest_framework.views import APIView

from vm_server.main_app.models import Item, User, VM, PyTerminal
from vm_server.main_app.serializers import ItemSerializer, UserSerializer, VMSerializer, PyTerminalSerializer


#  new

def index(request):
    return render(request, 'core/index.html')


def test(request):
    return render(request, 'main_app/test.html')


@api_view(['GET'])
def get_data(request):
    all_objects = Item.objects.all()
    serializer = ItemSerializer(
        all_objects,
        many=True,      # if many=True, if only 1=False
    )
    return Response(
        serializer.data,    # we want the .data
    )


@api_view(['GET'])
def get_item(request, identifier):
    try:
        # First, try to get by ID (numeric identifier)
        item = Item.objects.get(pk=identifier)
    except (Item.DoesNotExist, ValueError):
        # If not found or not numeric, try to get by name
        try:
            item = Item.objects.get(name=identifier)
        except Item.DoesNotExist:
            return Response({'error': 'Item not found'}, status=404)

    serializer = ItemSerializer(item)
    return Response(serializer.data)


@api_view(['POST'])
def add_item(request):
    serializer = ItemSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

# add and edit (POST/PUT, in postman: body --> raw --> JSON) like this:
"""
{
"username":"Daniel Zorov",
"password":"1",
"is_admin": false
}
"""


@api_view(['DELETE'])
def delete_item(request, identifier):
    try:
        # First, try to delete by ID (numeric identifier)
        item = Item.objects.get(pk=identifier)
    except (Item.DoesNotExist, ValueError):
        # If not found or not numeric, try to delete by name
        try:
            item = Item.objects.get(name=identifier)
        except Item.DoesNotExist:
            return Response({'error': 'Item not found'}, status=404)

    item.delete()
    return Response({'message': 'Item deleted successfully'})


@api_view(['PUT', 'PATCH'])
def update_item(request, identifier):
    try:
        item = Item.objects.get(pk=identifier)
    except Item.DoesNotExist:
        return Response({'error': 'Item not found'}, status=404)

    serializer = ItemSerializer(item, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)


# ---------------------------------------------------------------------------------
# Functions related to other scripts
# ---------------------------------------------------------------------------------
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

# ---------------------------------------------------------------------------------
# User
# ---------------------------------------------------------------------------------
@api_view(['GET'])
def get_users_list(request):
    all_objects = User.objects.all()
    serializer = UserSerializer(all_objects, many=True)

    custom_function()

    return Response(serializer.data)


@api_view(['GET'])
def show_user(request, identifier):
    try:
        user = User.objects.get(pk=identifier)
    except (User.DoesNotExist, ValueError):
        try:
            user = User.objects.get(username=identifier)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)

    serializer = UserSerializer(user)
    return Response(serializer.data)


@api_view(['PUT', 'PATCH'])
def edit_user(request, identifier):
    try:
        user = User.objects.get(pk=identifier)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)

    serializer = UserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)


@api_view(['DELETE'])
def delete_user(request, identifier):
    try:
        user = User.objects.get(pk=identifier)
    except (User.DoesNotExist, ValueError):
        try:
            user = User.objects.get(username=identifier)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)

    user.delete()
    return Response({'message': 'User deleted successfully'})


@api_view(['POST'])
def add_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


# ---------------------------------------------------------------------------------
# VM
# ---------------------------------------------------------------------------------
@api_view(['GET'])
def get_vms_list(request):
    all_objects = VM.objects.all()
    serializer = VMSerializer(all_objects, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def show_vm(request, identifier):
    try:
        vm = VM.objects.get(pk=identifier)
    except (VM.DoesNotExist, ValueError):
        try:
            vm = VM.objects.get(vm_name=identifier)
        except VM.DoesNotExist:
            return Response({'error': 'VM not found'}, status=404)

    serializer = VMSerializer(vm)
    return Response(serializer.data)


@api_view(['PUT', 'PATCH'])
def edit_vm(request, identifier):
    try:
        vm = VM.objects.get(pk=identifier)
    except VM.DoesNotExist:
        return Response({'error': 'VM not found'}, status=404)

    serializer = VMSerializer(vm, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)


@api_view(['DELETE'])
def delete_vm(request, identifier):
    try:
        vm = VM.objects.get(pk=identifier)
    except (VM.DoesNotExist, ValueError):
        try:
            vm = VM.objects.get(vm_name=identifier)
        except VM.DoesNotExist:
            return Response({'error': 'VM not found'}, status=404)

    vm.delete()
    return Response({'message': 'VM deleted successfully'})


@api_view(['POST'])
def add_vm(request):
    serializer = VMSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


# ---------------------------------------------------------------------------------
# PyTerminal
# ---------------------------------------------------------------------------------
@api_view(['GET'])
def get_pyterminals_list(request):
    all_objects = PyTerminal.objects.all()
    serializer = PyTerminalSerializer(all_objects, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def show_pyterminal(request, identifier):
    try:
        pyterminal = PyTerminal.objects.get(pk=identifier)
    except (PyTerminal.DoesNotExist, ValueError):
        try:
            pyterminal = PyTerminal.objects.get(terminal_name=identifier)
        except PyTerminal.DoesNotExist:
            return Response({'error': 'PyTerminal not found'}, status=404)

    serializer = PyTerminalSerializer(pyterminal)
    return Response(serializer.data)


@api_view(['PUT', 'PATCH'])
def edit_pyterminal(request, identifier):
    try:
        pyterminal = PyTerminal.objects.get(pk=identifier)
    except PyTerminal.DoesNotExist:
        return Response({'error': 'PyTerminal not found'}, status=404)

    serializer = PyTerminalSerializer(pyterminal, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)


@api_view(['DELETE'])
def delete_pyterminal(request, identifier):
    try:
        pyterminal = PyTerminal.objects.get(pk=identifier)
    except (PyTerminal.DoesNotExist, ValueError):
        try:
            pyterminal = PyTerminal.objects.get(terminal_name=identifier)
        except PyTerminal.DoesNotExist:
            return Response({'error': 'PyTerminal not found'}, status=404)

    pyterminal.delete()
    return Response({'message': 'PyTerminal deleted successfully'})


@api_view(['POST'])
def add_pyterminal(request):
    serializer = PyTerminalSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


# ---------------------------------------------------------------------------------
# Login
# ---------------------------------------------------------------------------------
def token_generator(username, password):
    token = username + password
    return token


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        print(f"Username: {username}, Password: {password}")

        all_users = User.objects.all()
        for user in all_users:
            if user.username == username and user.password == password:
                # generate an unique token for the user
                token = token_generator(username, password)
                print(token)

                return Response({
                    'token': token,
                    'username': user.username,
                    'id': user.id,
                    'is_admin': user.is_admin,
                })
        return Response({'error': 'Wrong Credentials'}, status=status.HTTP_400_BAD_REQUEST)
# ---------------------------------------------------------------------------------
