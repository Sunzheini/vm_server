from django.db import models
from picklefield.fields import PickledObjectField


class VBControllerInstance(models.Model):
    name = models.CharField(max_length=50)
    serialized_controller = PickledObjectField()

    def __str__(self):
        return self.name
