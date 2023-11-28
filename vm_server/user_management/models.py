from django.db import models


class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.username
