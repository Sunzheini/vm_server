from unittest import TestCase
from controllers.vb_controller import VBController


class VBControllerTests(TestCase):
    """
    Test all methods of the VBController class
    """

    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        self.vb_controller_instance = None

    def test_create_vb_controller_instance__expect_to_create(self):
        # Arrange

        # Act
        self.vb_controller_instance = VBController()

        # Assert
        self.assertIsNotNone(self.vb_controller_instance)
        self.assertIsNotNone(self.vb_controller_instance.vbox)
        self.assertIsNotNone(self.vb_controller_instance.session)

    def test_initiate_machine__with_correct_machine_name__expect_to_start(self):
        # Arrange
        self.vb_controller_instance = VBController()
        vm_name = 'TwinCAT'

        # Act
        result = self.vb_controller_instance.initiate_machine(vm_name)

        # Assert
        self.assertEqual(result, "Success")

    def tearDown(self):
        try:
            self.vb_controller_instance.close()
        except:
            pass
