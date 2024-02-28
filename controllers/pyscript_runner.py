import os
import subprocess

from vm_server import settings


class PyScriptRunner:
    """
    This class is responsible for running the pyscript. It is called by the
    engine and returns a string with the result of the execution.
    """
    @staticmethod
    def _get_the_absolute_path(script_name: str) -> str:
        """
        Returns the absolute path of the script.
        @param script_name: The name of the script, i.e. `hello_world.py`
        @return: The absolute path of the script
        """
        try:
            script_path = os.path.join(settings.MEDIA_ROOT, str(script_name))
        except Exception as e:
            return f'Error: {e}'
        return script_path

    def _check_if_script_exists(self, script_name: str) -> bool:
        """
        Checks if the script exists.
        @param script_name: The name of the script, i.e. `hello_world.py`
        @return: True if the script exists, False otherwise
        """
        script_path = self._get_the_absolute_path(script_name)
        return os.path.exists(script_path)

    def run_script(self, script_name: str) -> str:
        """
        Runs the script and returns the result of the execution.
        First it gets the absolute path of the script, then it runs it.
        The relative path looks like `uploads/hello_world.py`.
        Then it executes it and returns the result
        @param script_name: The name of the script, i.e. `hello_world.py`
        The script should print the result, i.e. `print('Hello World')`
        and then this result will be returned by this method and
        displayed in the frontend.
        @return: The result of the execution
        """
        # check if the script_name is not None
        if not script_name:
            return 'Error: The script name is None'

        # get the absolute path of the script
        try:
            if not self._check_if_script_exists(script_name):
                raise Exception('The script does not exist')

            script_path = self._get_the_absolute_path(script_name)
        except Exception as e:
            return f'Error (get_the_absolute_path): {e}'

        # execute the script and get its result
        try:
            result = subprocess.run([
                'python', script_path,
            ], capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout
            else:
                return f'Error (execution): {result.stderr}'
        except Exception as e:
            return f'Error (try-except): {e}'
