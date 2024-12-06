from django.db import models
from bookings.models import Booking

class Payment(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    payment_date = models.DateField()

    def __str__(self):
        return f"Payment for Booking {self.booking.id} - {self.amount}"
