"""
These constants are used to define the paths to the DLLs and the classes that are imported from them.
They are used by the dll_runner class.
"""

framework_dll_path = r'C:\Appl\Projects\C#\testrunner-interfaces\Festo.AST.Testrunner.Interfaces\Festo.AST.Testrunner.Interfaces.NFCL\bin\Debug'
framework_dll_name = 'Festo.AST.Testrunner.Interfaces.NFCL'
framework_dll_imports = [
    {
        'Festo.AST.Testrunner.Interfaces.NFCL.Entities': [
            'Device',
            'Project',
        ]
    },
    {
        'Festo.AST.Testrunner.Interfaces.NFCL.Utils': [
            'JsonMethodsCollection',
            'RestCommandsCollection',
        ]
    },
    {
        'Festo.AST.Testrunner.Interfaces.NFCL.G0_ConfigurationPlc': [
            'G00_RequestPlcMetaData',
            'G01_ResponsePlcMetaData',
        ]
    }
]

core_dll_path = r'C:\Appl\Projects\C#\testrunner-interfaces\Festo.AST.Testrunner.Interfaces\Festo.AST.Testrunner.Interfaces\bin\Debug\net6.0'
core_dll_name = 'Festo.AST.Testrunner.Interfaces'
core_dll_imports = [
    {
        'Festo.AST.Testrunner.Interfaces.Entities': [
            'DataRecording',
            'Device',
            'Plc',
            'Project',
            'SingleLogEntry',
            'Test',
            'VersionInfoPacket',
        ]
    },
    {
        'Festo.AST.Testrunner.Interfaces.G0_ConfigurationPlc': [
            'G00_RequestPlcMetaData',
            'G01_ResponsePlcMetaData',
            'G02_RequestPlcConfigure',
            'G03_ResponsePlcConfigure',
        ]
    }
]
