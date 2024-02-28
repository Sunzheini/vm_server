import unittest
from unittest import TestCase


class TestPyscriptRunner(TestCase):
    """
    Test all methods of the PyscriptRunner class
    """
    # once before all tests
    @classmethod
    def setUpClass(cls):
        pass

    # before each test
    def setUp(self):
        from controllers.pyscript_runner import PyScriptRunner
        self.runner = PyScriptRunner()

    # what_you_do__how_you_do_it__expected_result (act__arrange__assert)
    def test_run_pyscript__receives_non_null_path__runs_it_correctly(self):
        # Arrange: prepare the data needed to run the test
        script_path = 'uploads/hello_world.py'
        expected_string = 'Hello world'

        # Act: execute the method you wish to test
        result = self.runner.run_script(script_path)

        # Assert: check if the result is as expected
        self.assertIn(expected_string, result)

    def test_run_pyscript__receives_null_path__return_error_string(self):
        # Arrange
        script_path = None
        error_message = 'Error: The script name is None'

        # Act
        result = self.runner.run_script(script_path)

        # Assert
        self.assertIn(error_message, result)

    def test_run_pyscript__receives_non_existing_path__return_error_string(self):
        # Arrange
        script_path = 'uploads/non_existing_script.py'
        error_message = 'Error'

        # Act
        result = self.runner.run_script(script_path)

        # Assert
        self.assertIn(error_message, result)
