from concurrent.futures.process import _python_exit
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    choices = (
    ('bus', 'Day Scholor'),
    ('hos', 'Hosteller'),
    ('inc', 'Transport department'),
    )
    user_type = models.CharField(max_length=3, choices=choices, default='bus', null=False, blank=False)

    def __str__(self):
        return f"{self.username} - {self.user_type}"