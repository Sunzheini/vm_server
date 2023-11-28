from django.db import models


class PyTerminal(models.Model):
    terminal_name = models.CharField(max_length=100, unique=True)
    is_py_open = models.BooleanField(default=False)
    current_command = models.CharField(max_length=100, blank=True, null=True)
    all_commands = models.TextField(blank=True, null=True)
    is_sent = models.BooleanField(default=False)

    def __str__(self):
        return self.terminal_name
