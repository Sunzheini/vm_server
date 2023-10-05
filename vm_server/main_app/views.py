from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view

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

# post like this:
"""
{
"name":"Item from post"
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
# User
# ---------------------------------------------------------------------------------

@api_view(['GET'])
def get_users_list(request):
    all_objects = User.objects.all()
    serializer = UserSerializer(all_objects, many=True)
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
