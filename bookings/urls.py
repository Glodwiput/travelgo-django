from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('', views.BookingListView.as_view(), name='booking_list'),  # Daftar Booking
    path('create/<int:pk>', views.create_booking, name='create_booking'),  # Buat Booking Baru
    path('update/<int:pk>/', views.update_booking, name='update_booking'),  # Update Booking
    path('delete/<int:pk>/', views.delete_booking, name='delete_booking'),
]
