from rest_framework import serializers

from vm_server.main_app.models import Item, User, VM, PyTerminal


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class VMSerializer(serializers.ModelSerializer):
    class Meta:
        model = VM
        fields = '__all__'


class PyTerminalSerializer(serializers.ModelSerializer):
    class Meta:
        model = PyTerminal
        fields = '__all__'
