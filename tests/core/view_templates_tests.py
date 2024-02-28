from django.test import TestCase
from rest_framework import request

from core.view_templates import ViewTemplates
from vm_server.virtual_machines.models import VM
from core.serializers import VMSerializer


class ViewTemplatesTests(TestCase):
    """
    Test all methods of the view_templates. In order for the tests to work,
    comment the @time_measurement_decorator in the view_templates.py file!
    """
    # once before all tests
    @classmethod
    def setUpClass(cls):
        pass

    # before each test
    def setUp(self):
        pass

    # what_you_do__how_you_do_it__expected_result (act__arrange__assert)
    def test_list_view_template__when_called__expect_to_return_data(self):
        # Arrange
        model = VM
        model_serializer = VMSerializer

        # Act
        response = ViewTemplates.list_view_template(model, model_serializer)

        # Assert
        self.assertEqual(response.status_code, 200)

    def test_create_view_template__with_correct_data__expect_to_create(self):
        # Arrange
        model_serializer = VMSerializer
        request.data = {'vm_name': 'test'}

        # Act
        response = ViewTemplates.create_view_template(model_serializer, request)

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['vm_name'], 'test')

    def test_create_view_template__with_incorrect_data__expect_to_raise_exception(self):
        # Arrange
        model_serializer = VMSerializer
        request.data = {'vm_name': ''}

        # Act
        response = ViewTemplates.create_view_template(model_serializer, request)

        # Assert
        self.assertEqual(response.status_code, 400)

    def test_show_view_template__with_correct_identifier__expect_to_return_data(self):
        # Arrange
        model = VM
        model_serializer = VMSerializer
        identifier = 1
        alternative_field_name = 'TwinCAT'
        new_vm = VM(vm_name=alternative_field_name)
        new_vm.full_clean()
        new_vm.save()

        # Act
        response = ViewTemplates.show_view_template(model, model_serializer, identifier, alternative_field_name)

        # Assert
        self.assertEqual(response.status_code, 200)

    def test_show_view_template__with_incorrect_identifier__expect_to_raise_exception(self):
        # Arrange
        model = VM
        model_serializer = VMSerializer
        identifier = 33
        alternative_field_name = 'TwinCAT'

        new_vm = VM(vm_name=alternative_field_name)
        new_vm.full_clean()
        new_vm.save()

        # Act
        response = ViewTemplates.show_view_template(model, model_serializer, identifier, alternative_field_name)

        # Assert
        self.assertEqual(response.status_code, 404)

    def test_edit_view_template__with_correct_identifier__expect_to_return_data(self):
        # Arrange
        model = VM
        model_serializer = VMSerializer
        identifier = 1
        alternative_field_name = 'TwinCAT'
        request.data = {'vm_name': 'test'}

        new_vm = VM(vm_name=alternative_field_name)
        new_vm.full_clean()
        new_vm.save()

        # Act
        response = ViewTemplates.edit_view_template(model, model_serializer, identifier, alternative_field_name, request)

        # Assert
        self.assertEqual(response.status_code, 200)

    def test_delete_view_template__with_correct_identifier__expect_to_delete(self):
        # Arrange
        model = VM
        identifier = 1
        alternative_field_name = 'TwinCAT'

        new_vm = VM(vm_name=alternative_field_name)
        new_vm.full_clean()
        new_vm.save()

        # Act
        response = ViewTemplates.delete_view_template(model, identifier, alternative_field_name)

        # Assert
        self.assertEqual(response.status_code, 200)

    # after each test
    def tearDown(self):
        pass

    # once after all tests
    @classmethod
    def tearDownClass(cls):
        pass