from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from bookings.models import Booking
from bus.models import Bus
from services.models import Service

from datetime import datetime
User = get_user_model()


class BookingTests(TestCase):

    def setUp(self):
        # Buat pengguna untuk login
        self.user = User.objects.create_user(username="testuser", password="password")
        self.bus = self.bus = Bus.objects.create(
            name="Test Bus",
            price=1000,
            seat=50,
            departure_time=datetime.now()  # Pass a valid datetime
        )
        self.service = Service.objects.create(name="Wi-Fi", price=50, is_active=True)

    def test_booking_list_view_authenticated_user(self):
        # Login dengan user
        self.client.login(username="testuser", password="password")
        
        # Buat booking
        booking = Booking.objects.create(
            user=self.user,
            bus=self.bus,
            seats=2,
            price_total=2000,
        )
        booking.services.set([self.service])
        
        # Akses halaman daftar booking
        response = self.client.get(reverse('bookings:booking_list'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Bus")
        self.assertContains(response, booking.user.username)
        self.assertContains(response, booking.seats)

    def test_create_booking_valid_data(self):
        self.client.login(username="testuser", password="password")
        
        data = {
            'seat': 2,
            'services': [self.service.id],
        }
        
        response = self.client.post(reverse('bookings:create_booking', kwargs={"pk": self.bus.id}), data)

        self.assertEqual(response.status_code, 200)  # Redirect ke halaman setelah berhasil membuat booking

    def test_update_booking_with_permission(self):
        # Buat booking dengan user
        booking = Booking.objects.create(
            user=self.user,
            bus=self.bus,
            seats=2,
            price_total=2000,
        )
        
        self.client.login(username="testuser", password="password")
        
        # Simulasikan POST request untuk mengupdate booking
        data = {
            'seats': 3,
            'services': [self.service.id],
        }
        
        response = self.client.post(reverse('bookings:update_booking', kwargs={"pk": booking.id}), data)
        
        self.assertEqual(response.status_code, 302)
        booking.refresh_from_db()
        self.assertEqual(booking.seats, 3)

    def test_delete_booking(self):
        # Buat booking yang bisa dihapus
        booking = Booking.objects.create(
            user=self.user,
            bus=self.bus,
            seats=2,
            price_total=2000,
        )
        
        self.client.login(username="testuser", password="password")
        
        response = self.client.post(reverse('bookings:delete_booking', kwargs={"pk": booking.id}))
        
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Booking.objects.filter(id=booking.id).exists())

#5
    def test_booking_error_too_many_seat(self):
        self.client.login(username="testuser", password="password")
        
        # Simulasikan data dengan kursi yang melebihi jumlah yang tersedia
        data = {
            'seats': 2,
            'services': [self.service.id],
        }

        response = self.client.post(reverse('bookings:create_booking', kwargs={"pk": self.bus.id}), data)
        
