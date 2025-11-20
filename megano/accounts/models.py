from django.db import models

class UserInfo(models.Model):
    name = models.CharField(max_length=100, unique=True, null=False, blank=False)
    username = models.CharField(max_length=100, null=False, blank=False)
    password = models.CharField(max_length=30, null=False, blank=False)

    def __str__(self):
        return self.username