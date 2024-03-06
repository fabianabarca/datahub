from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class User(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.CharField(max_length=100)
    position = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username
