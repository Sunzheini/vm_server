from django.db import models


# for testing
class Item(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# actual models
class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class VM(models.Model):
    vm_name = models.CharField(max_length=100, unique=True)
    vm_status = models.TextField(blank=True, null=True)

    is_started = models.BooleanField(default=False)
    is_compiled = models.BooleanField(default=False)
    is_downloaded = models.BooleanField(default=False)
    is_online = models.BooleanField(default=False)
    is_running = models.BooleanField(default=False)
    is_enabled = models.BooleanField(default=False)

    param_name = models.CharField(max_length=100, blank=True, null=True)
    param_value = models.CharField(max_length=100, blank=True, null=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.vm_name


class PyTerminal(models.Model):
    terminal_name = models.CharField(max_length=100, unique=True)
    is_py_open = models.BooleanField(default=False)
    current_command = models.CharField(max_length=100, blank=True, null=True)
    all_commands = models.TextField(blank=True, null=True)
    is_sent = models.BooleanField(default=False)

    def __str__(self):
        return self.terminal_name
