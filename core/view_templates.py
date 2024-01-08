from rest_framework.response import Response

from core.decorators import time_measurement_decorator
from core.engine import Engine


class ViewTemplates:
    @staticmethod
    @time_measurement_decorator
    def list_view_template(model, model_serializer):
        """
        A template for a list view
        @param model:
        @param model_serializer:
        @return: A response with all objects of the model
        """
        all_objects = model.objects.all()
        serializer = model_serializer(all_objects, many=True)
        return Response(serializer.data)

    @staticmethod
    @time_measurement_decorator
    def create_view_template(model_serializer, request):
        """
        A template for a create view=.
        @param model_serializer:
        @param request:
        @return: A response with the created object
        """
        serializer = model_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    @staticmethod
    @time_measurement_decorator
    def show_view_template(model, model_serializer, identifier, alternative_field_name):
        """
        A template for a show view
        @param model:
        @param model_serializer:
        @param identifier:
        @param alternative_field_name:
        @return: A response with the object
        """
        try:
            # First, try to get by ID (numeric identifier)
            item = model.objects.get(pk=identifier)
        except (model.DoesNotExist, ValueError):
            # If not found or not numeric, try to get by alternative_field_name
            try:
                item = model.objects.get(alternative_field_name=identifier)
            except model.DoesNotExist:
                return Response({'error': f'{model} not found'}, status=404)

        serializer = model_serializer(item)
        return Response(serializer.data)

    @staticmethod
    @time_measurement_decorator
    def edit_view_template(model, model_serializer, identifier, alternative_field_name, request):
        """
        A template for an edit view. Bound to a method of the Engine class, which is called after
        the object is saved. The method decides if other actions are needed, based
        on the object's fields.
        @param model:
        @param model_serializer:
        @param identifier:
        @param alternative_field_name:
        @param request:
        @return: A response with the updated object
        """
        try:
            # First, try to get by ID (numeric identifier)
            item = model.objects.get(pk=identifier)
        except (model.DoesNotExist, ValueError):
            # If not found or not numeric, try to get by alternative_field_name
            try:
                item = model.objects.get(alternative_field_name=identifier)
            except model.DoesNotExist:
                return Response({'error': f'{model} not found'}, status=404)

        serializer = model_serializer(item, data=request.data, partial=True)

        if serializer.is_valid():
            # check if model is VM or PyScript, which need special treatment
            if model.__name__ == 'VM' or model.__name__ == 'PyScript':
                Engine.update_the_model(model, item, serializer)

            # for the other models
            else:
                serializer.save()

            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    @staticmethod
    @time_measurement_decorator
    def delete_view_template(model, identifier, alternative_field_name):
        """
        A template for a delete view
        @param model:
        @param identifier:
        @param alternative_field_name:
        @return: A response with a message of success or failure to delete
        """
        try:
            # First, try to delete by ID (numeric identifier)
            item = model.objects.get(pk=identifier)
        except (model.DoesNotExist, ValueError):
            # If not found or not numeric, try to delete by alternative_field_name
            try:
                item = model.objects.get(alternative_field_name=identifier)
            except model.DoesNotExist:
                return Response({'error': f'{model} not found'}, status=404)

        item.delete()
        return Response({'message': f'{model} deleted successfully'})
