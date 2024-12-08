from django.views.generic import ListView
from bus.models import Bus
from .forms import BookingForm
from .models import Booking
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404

class BookingListView(ListView):
    model = Booking
    template_name = 'bookings/booking_list.html'

    def get(self, request, *args, **kwargs):
        booking = Booking.objects.filter(user=self.request.user)
        return render(request, self.template_name, {'bookings': booking})





def create_booking(request, pk):
    bus = Bus.objects.get(id=pk)
    
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            seats_requested = form.cleaned_data['seats']
            if bus.is_seat_available(seats_requested):
                
                booking = form.save(commit=False)
                booking.user = request.user
                booking.bus = bus

                
                ticket_price = seats_requested * bus.price
                
                selected_services = form.cleaned_data['services']
                service_price = sum(service.price for service in selected_services)

                
                booking.price_total = ticket_price + service_price
                booking.save()

                
                booking.services.set(selected_services)

                
                bus.reserve_seat(seats_requested)

                
                form.cleaned_data['services']
                booking.services.set(form.cleaned_data['services'])

                return redirect('bus:bus_list_customer')
            else:
                
                return render(request, 'bookings/create_booking.html', {
                    'form': form,
                    'error': 'The number of seats requested exceeds the number of seats available.'
                })
            return redirect('bus:bus_list_customer')
    else:
        form = BookingForm()
    
    return render(request, 'bus/bus_customer_list.html', {'form': form, 'bus':bus})



def update_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk)

    
    if booking.user != request.user:
        return HttpResponseForbidden("You are not allowed to edit this booking.")
    
    if request.method == "POST":
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            seats_requested = form.cleaned_data['seats']
            bus = booking.bus

            
            if bus.is_seat_available(seats_requested, exclude_booking=booking):
                
                booking = form.save(commit=False)
                booking.price_total = seats_requested * bus.price  # Hitung ulang harga tiket
                service_price = sum(service.price for service in form.cleaned_data['services'])
                booking.price_total += service_price
                booking.save()
                booking.services.set(form.cleaned_data['services'])
                return redirect('bookings:booking_list')
            else:
                return render(request, 'bookings/update_booking.html', {
                    'form': form,
                    'error': 'The number of seats requested exceeds the number of seats available.'
                })
    else:
        form = BookingForm(instance=booking)
    
    return render(request, 'bookings/update_booking.html', {'form': form, 'booking': booking})


def delete_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk)

    
    if booking.user != request.user:
        return HttpResponseForbidden("You are not allowed to delete this booking.")
    
    if request.method == "POST":
        
        bus = booking.bus
        bus.release_seat(booking.seats)
        booking.delete()
        return redirect('bookings:booking_list')
    
    return render(request, 'bookings/delete_booking.html', {'booking': booking})
