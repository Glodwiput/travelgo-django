from django.db import models

class Bus(models.Model):
    name = models.CharField(max_length=100)
    departure = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_time = models.DateTimeField()
    seat = models.IntegerField()
    description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.URLField()

    def __str__(self):
        return f"{self.name} - {self.departure} to {self.destination}"
    
    def release_seat(self, seats):
        self.seat += seats
        self.save()

    def is_seat_available(self, seats, exclude_booking=None):
        reserved_seats = 0
        if exclude_booking:
            reserved_seats = exclude_booking.seats
        return self.seat + reserved_seats >= seats

    def reserve_seat(self, seats_requested):
        self.seat -= seats_requested
        self.save()
