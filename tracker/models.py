from concurrent.futures.process import _python_exit
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Q

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


class Announcements(models.Model):
    title = models.CharField(max_length=100)
    for_user = models.ForeignKey(User,max_length=3, limit_choices_to=Q(user_type="hos") | Q(user_type="bus"), default='bus', on_delete=models.CASCADE, related_name="announcements")
    description = models.TextField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.date}"

class Stops(models.Model):
    stop_no = models.IntegerField(primary_key=True)
    stop_name = models.CharField(max_length=100)
    stop_lat = models.FloatField(null=True, blank=True)
    stop_long = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.stop_no} - {self.stop_name}"

class Route(models.Model):
    route_no = models.IntegerField(primary_key=True)
    stops = models.ManyToManyField(Stops, related_name="routes")

    def __str__(self):
        return f"{self.route_no}"

class Bus(models.Model):
    bus_no = models.IntegerField(primary_key=True)
    bus_route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name="buses")

class BusCoordinates(models.Model):
    bus_no = models.CharField(max_length=10)
    latitude = models.CharField(max_length=20)
    longitude = models.CharField(max_length=20)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bus_no} - {self.date}"

class Bookings(models.Model):
    user = models.ForeignKey(User, limit_choices_to={'user_type': 'hos'}, on_delete=models.CASCADE, related_name="bookings")
    bus_no = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name="bookings")
    date = models.DateField(auto_now_add=True)
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name="bookings")