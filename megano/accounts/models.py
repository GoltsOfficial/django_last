from django.contrib.auth.hashers import make_password, check_password
from django.db import models


class UserInfo(models.Model):
    name = models.CharField(max_length=100, unique=True)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=128)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self.save()

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
