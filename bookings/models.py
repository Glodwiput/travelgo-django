from django.db import models
from django.conf import settings
from bus.models import Bus
from users.models import User
from services.models import Service


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    seats = models.PositiveIntegerField()
    services = models.ManyToManyField(Service, blank=True) 

class Payment(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    payment_date = models.DateField()

    def __str__(self):
        return f"Payment for Booking {self.booking.id} - {self.amount}"