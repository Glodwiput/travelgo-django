from django.db import models

class Bus(models.Model):
    name = models.CharField(max_length=100)
    departure = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_time = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

class Seat(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=10)
    is_available = models.BooleanField(default=True)
