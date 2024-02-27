from rest_framework import serializers

from vm_server.user_management.models import User
from vm_server.virtual_machines.models import VM
from vm_server.py_scripts.models import PyScript
from vm_server.py_terminals.models import PyTerminal


"""
These are the serializers for the models: User, VM, PyScript, PyTerminal.
"""


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class VMSerializer(serializers.ModelSerializer):
    class Meta:
        model = VM
        fields = '__all__'


class PyScriptSerializer(serializers.ModelSerializer):
    class Meta:
        model = PyScript
        fields = '__all__'


class PyTerminalSerializer(serializers.ModelSerializer):
    class Meta:
        model = PyTerminal
        fields = '__all__'


# ---------------------------------------------------------------
# needed to get the vm types for the list of choices when creating a new vm
# ---------------------------------------------------------------
class VMTypeSerializer(serializers.Serializer):
    vm_type = serializers.CharField()
