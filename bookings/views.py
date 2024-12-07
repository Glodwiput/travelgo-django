from django.views.generic import ListView
from .models import Booking
from django.shortcuts import render, redirect
from .forms import BookingForm
from bus.models import Bus


class BookingListView(ListView):
    model = Booking
    template_name = 'bookings/booking_list.html'

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)


def create_bookings(request, bus_id):
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.bus_id = bus_id
            booking.save()
            return redirect('bookings:booking_list')
    else:
        form = BookingForm()
    return render(request, 'bookings/create_booking.html', {'form': form})

from django.shortcuts import render, redirect
from .forms import BookingForm
from .models import Booking


def create_booking(request, pk):
    bus = Bus.objects.get(id=pk)
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            seats_requested = form.cleaned_data['seats']
            if bus.is_seat_available(seats_requested):
                # Jika kursi tersedia
                booking = form.save(commit=False)
                booking.user = request.user
                booking.bus = bus
                booking.save()

                # Kurangi kursi pada bus
                bus.reserve_seat(seats_requested)

                # Jika layanan tambahan dipilih
                form.cleaned_data['services']
                booking.services.set(form.cleaned_data['services'])

                return redirect('bookings:booking_list')
            else:
                # Jika tidak ada cukup kursi
                return render(request, 'bookings/create_booking.html', {
                    'form': form,
                    'error': 'Jumlah kursi yang diminta melebihi jumlah kursi yang tersedia.'
                })
            return redirect('bookings:booking_list')
    else:
        form = BookingForm()
    
    return render(request, 'bookings/create_booking.html', {'form': form})

