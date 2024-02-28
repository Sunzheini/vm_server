import clr
import sys
import os


class DllRunner:
    """
    This class is used to register dlls and import classes from the corresponding namespaces.
    You can then use the classes as attributes of the DllRunner object.
    """
    def __init__(self, dll_path: str = None, dll_name: str = None, dll_imports: list = None):
        self._dll_folder_path = os.path.abspath(dll_path)
        self._dll_name = dll_name
        self._dll_imports = dll_imports

        self._register_dll()
        self._handle_imports(*self._dll_imports)

    def _register_dll(self):
        """
        Register the dll name and adds the path to the dll folder to the sys.path
        :param dll_name: name of the dll must be usable by python, not i.e. "09.Some text", but
        "Festo.AST.Testrunner.Interfaces.NFCL" or "System.Windows.Forms"
        :param dll_folder_path: path to the dll folder, where the dll is located
        """
        sys.path.append(self._dll_folder_path)
        clr.AddReference(self._dll_name)

    def _handle_imports(self, *args):
        """
        Imports classes from the corresponding namespaces
        :param args: it is a list of dictionaries, where the key is the namespace and the value is a list of classes
        The name of the namespace must be something like "Festo.AST.Testrunner.Interfaces".
        The name of the class must be something like "Device" and it must be public. Can also be a static class.
        """
        # Internal method to import classes
        for arg in args:
            for namespace, classes in arg.items():
                for class_name in classes:
                    exec(f"from {namespace} import {class_name}")
                    setattr(self, class_name, eval(class_name))

    @staticmethod
    def translate_python_list_to_dotnet_generic_list(python_list, type_of_list):
        """
        Translates a Python list to a .NET List<T>
        Example:
        dotnet_device_list = runner.translate_python_list_to_dotnet_generic_list(
                [runner.Device('id1', '1', '1'), runner.Device('id2', '2', '2')],
                runner.Device
            )
        :param type_of_list: the type of the list, i.e. list of objects of type Device
        :param python_list: Python list
        :return: .NET List<T>
        """
        dotnet_list = clr.System.Collections.Generic.List[type_of_list]()
        [dotnet_list.Add(item) for item in python_list]
        return dotnet_list

    @staticmethod
    def translate_dotnet_generic_list_to_python_list(dotnet_list):
        """
        Translates a .NET List<T> to a Python list
        :param dotnet_list: .NET List<T>
        :return: Python list
        """
        python_list = []
        [python_list.append(item) for item in dotnet_list]
        return python_list
