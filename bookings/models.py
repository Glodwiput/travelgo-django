from django.db import models
from django.conf import settings
from bus.models import Bus
from users.models import User

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    seats = models.PositiveIntegerField()

# class Payment(models.Model):
#     booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     status = models.CharField(max_length=50)
#     created_at = models.DateTimeField(auto_now_add=True)
