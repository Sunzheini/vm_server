from unittest import TestCase
from constants.constants import core_dll_path, core_dll_name, core_dll_imports
from core.dll_runner import DllRunner


class TestDllRunner(TestCase):
    """
    Test all methods of the DllRunner class
    """
    # once before all tests
    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        self.dll_path = core_dll_path
        self.dll_name = core_dll_name
        self.imports = core_dll_imports
        self.runner = None

    def test_dll_runner_object__with_correct_args__initiates_properly(self):
        # Arrange
        dll_path = self.dll_path
        dll_name = self.dll_name
        imports = self.imports

        # Act
        self.runner = DllRunner(dll_path, dll_name, imports)

        # Assert
        self.assertEqual(self.runner._dll_folder_path, dll_path)

    def test_dll_runner_object__with_incorrect_dll_name__raises_exception(self):
        # Arrange
        dll_path = self.dll_path
        dll_name = 'incorrect_dll_name'
        imports = self.imports

        # Act & Assert
        with self.assertRaises(Exception):
            self.runner = DllRunner(dll_path, dll_name, imports)

    def test_dll_runner_object__with_incorrect_imports__raises_exception(self):
        # Arrange
        dll_path = self.dll_path
        dll_name = self.dll_name
        imports = 'incorrect_imports'

        # Act & Assert
        with self.assertRaises(Exception):
            self.runner = DllRunner(dll_path, dll_name, imports)

    def tearDown(self):
        self.runner = None
