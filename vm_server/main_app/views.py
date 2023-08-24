from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view

from vm_server.main_app.models import Item
from vm_server.main_app.serializers import ItemSerializer


"""
can upload .py scripts which will be executed on the server
"""


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
