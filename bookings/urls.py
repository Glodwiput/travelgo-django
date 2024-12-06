from django.urls import path
from . import views

urlpatterns = [
    path('', views.BookingListView.as_view(), name='booking_list'),  # Daftar Booking
    path('create/<int:bus_id>/', views.create_booking, name='create_booking'),  # Buat Booking Baru
]
