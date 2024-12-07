from django.db import models

class Bus(models.Model):
    name = models.CharField(max_length=100)
    departure = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_time = models.DateTimeField()
    seat = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.departure} to {self.destination}"
    
    def is_seat_available(self, seats_requested):
        """Cek apakah kursi yang diminta masih tersedia"""
        return self.seat >= seats_requested

    def reserve_seat(self, seats_requested):
        """Kurangi kursi sesuai jumlah yang dibooked"""
        self.seat -= seats_requested
        self.save()
