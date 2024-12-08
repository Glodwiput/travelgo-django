from django.db import models
from bookings.models import Booking
from bus.models import Bus

from django.conf import settings

class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='reviews', default=9)  
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE,  related_name='review')
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.booking} - {self.comment}"
