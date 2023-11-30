from django.db import models


class PyScript(models.Model):
    script_name = models.CharField(max_length=100, unique=True)
    script_file = models.FileField(upload_to='uploads/', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    script_is_executed = models.BooleanField(default=False)

    script_status = models.TextField(blank=True, null=True)

    def update_status(self, message_update):
        self.script_status = message_update
        self.save()
        return self.script_status

    def __str__(self):
        return f"{self.script_name}, {self.id}"
