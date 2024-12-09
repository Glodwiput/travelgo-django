from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from bus.models import Bus

User = get_user_model()

from django.urls import reverse
from django.test import TestCase
from django.utils import timezone


class BusListViewTest(TestCase):
    def test_add_bus_view(self):
        self.client.login(username='admin_user', password='password')
        response = self.client.post(reverse('bus:bus_add'), {
            'name': 'Bus Test',
            'departure': 'Jakarta',
            'destination': 'Bandung',
            'departure_time': timezone.now(),
            'seat': 20,
            'description': 'Test bus',
            'price': '150.00',
            'image': 'http://example.com/image.jpg',
        })
        self.assertEqual(response.status_code, 302)

    def test_update_bus_view(self):
        self.client.login(username='admin_user', password='password')
        bus = Bus.objects.create(
            name='Bus Update',
            departure='Jakarta',
            destination='Bandung',
            departure_time=timezone.now(),
            seat=20,
            description='Test bus',
            price='150.00',
            image='http://example.com/image.jpg',
        )
        response = self.client.post(reverse('bus:bus_update', args=[bus.pk]), {
            'name': 'Updated Bus',
            'departure': 'Jakarta',
            'destination': 'Yogyakarta',
            'departure_time': timezone.now(),
            'seat': 25,
            'description': 'Updated',
            'price': '200.00',
            'image': 'http://example.com/image_updated.jpg',
        })
        self.assertEqual(response.status_code, 302)

# test 2
class TestAddBusView(TestCase):
    def setUp(self):
        self.staff_user = User.objects.create_user(
            username="staff_user", 
            password="password"
        )

    def test_add_bus_view(self):
        # Login sebagai staff user
        self.client.login(username="staff_user", password="password")
        # Simulasi POST request untuk menambahkan bus
        bus_data = {
            "name": "Bus 3",
            "departure": "Jakarta",
            "destination": "Medan",
            "departure_time": "2023-12-25 08:00",
            "seat": 20,
            "description": "Bus test",
            "price": "120.00",
            "image": "http://example.com/image"
        }
        response = self.client.post(reverse('bus:bus_add'), data=bus_data)
        self.client.logout()

#test 3
class TestUpdateBusView(TestCase):
    def setUp(self):
        self.staff_user = User.objects.create_user(
            username="staff_user", 
            password="password"
        )
        self.bus = Bus.objects.create(
            name="Bus 4",
            departure="Jakarta",
            destination="Yogyakarta",
            departure_time="2023-12-25 09:00",
            seat=30,
            description="Test bus",
            price=200,
            image="http://example.com/image"
        )

    def test_update_bus_view(self):
        self.client.login(username="staff_user", password="password")
        update_data = {
            "name": "Updated Bus Name",
            "departure": "Jakarta",
            "destination": "Bali",
            "departure_time": "2024-01-01 10:00",
            "seat": 50,
            "description": "Updated Test bus",
            "price": 220,
            "image": "http://example.com/image_updated"
        }
        response = self.client.post(reverse('bus:bus_update', kwargs={'pk': self.bus.pk}), data=update_data)
        self.client.logout()

#test 4
class TestDeleteBusView(TestCase):
    def setUp(self):
        self.staff_user = User.objects.create_user(
            username="staff_user", 
            password="password"
        )
        self.bus = Bus.objects.create(
            name="Bus 5",
            departure="Jakarta",
            destination="Bandung",
            departure_time="2023-12-25 10:00",
            seat=30,
            description="Bus for delete test",
            price=200,
            image="http://example.com/image"
        )

    def test_delete_bus_view(self):
        self.client.login(username="staff_user", password="password")
        response = self.client.post(reverse('bus:bus_delete', kwargs={'pk': self.bus.pk}))
        self.client.logout()

#test 5
class TestBusCustomerListView(TestCase):
    def setUp(self):
        # Membuat contoh bus untuk diuji
        for i in range(20):
            Bus.objects.create(
                name=f"Bus {i}",
                departure="Jakarta",
                destination="Surabaya",
                departure_time="2023-12-20 08:00",
                seat=50,
                description="Search test",
                price=150,
                image="http://example.com/image"
            )

    def test_search_functionality(self):
        response = self.client.get(reverse('bus:bus_list_customer'), {"search": "Bus 1"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Bus 1")

    def test_pagination(self):
        response = self.client.get(reverse('bus:bus_list_customer'), {"page": 2})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context['buses']) > 0)
