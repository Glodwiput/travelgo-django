from django.views.generic import ListView
from .models import Booking
from django.shortcuts import render, redirect
from .forms import BookingForm

class BookingListView(ListView):
    model = Booking
    template_name = 'bookings/booking_list.html'

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)


def create_booking(request, bus_id):
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.bus_id = bus_id
            booking.save()
            return redirect('booking_list')
    else:
        form = BookingForm()
    return render(request, 'bookings/create_booking.html', {'form': form})
