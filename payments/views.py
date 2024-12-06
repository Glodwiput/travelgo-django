from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Payment
from bookings.models import Booking
from .forms import PaymentForm

class PaymentFormView(View):
    template_name = 'payment/payment_form.html'

    def get(self, request, booking_id):
        # Mendapatkan booking berdasarkan ID
        booking = get_object_or_404(Booking, id=booking_id)
        form = PaymentForm(initial={'booking': booking})
        return render(request, self.template_name, {'form': form, 'booking': booking})

    def post(self, request, booking_id):
        # Mendapatkan booking berdasarkan ID
        booking = get_object_or_404(Booking, id=booking_id)
        form = PaymentForm(request.POST)

        if form.is_valid():
            payment = form.save(commit=False)
            payment.booking = booking
            payment.save()
            return redirect('booking_list')  # Redirect ke daftar booking setelah pembayaran berhasil

        return render(request, self.template_name, {'form': form, 'booking': booking})
