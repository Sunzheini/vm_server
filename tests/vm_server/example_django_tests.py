from django.test import TestCase
from django.urls import reverse
from vm_server.user_management.models import User
from vm_server.virtual_machines.models import VM


class TestExampleClass(TestCase):
    """
    Test all methods of the example class
    """
    # once before all tests
    @classmethod
    def setUpClass(cls):
        pass

    # before each test
    def setUp(self):
        pass

    # what_you_do__how_you_do_it__expected_result (act__arrange__assert)
    def test_create_user__when_data_correct__expect_to_create(self):
        # Arrange: prepare the data needed to run the test
        new_user = User(username='test', password='test', is_admin=False)

        # Act: execute the method you wish to test
        new_user.full_clean()   # will raise exception if the data not valid
        new_user.save()

        # Assert: check if the result is as expected
        self.assertIsNotNone(new_user.id)

    def test_create_user__when_data_incorrect__expect_to_raise_exception(self):
        # Arrange
        new_user = User()

        # Act
        with self.assertRaises(Exception) as context:
            new_user.full_clean()

        # Assert
        # self.assertIsNotNone(context.exception)     # too generic
        self.assertTrue('username' in str(context.exception))

    # https://www.django-rest-framework.org/api-guide/testing/
    # added env vars to edit configuration of the test
    def test_get_vms_list__when_called__expect_to_return_all_vms(self):
        # Arrange
        # Since the test is using a fake database, we need to create a VM object
        new_vm = VM(vm_name='test')
        new_vm.full_clean()
        new_vm.save()

        # Act
        response = self.client.get(reverse('get vms list'))

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['vm_name'], 'test')

    # after each test
    def tearDown(self):
        pass

    # once after all tests
    @classmethod
    def tearDownClass(cls):
        pass
