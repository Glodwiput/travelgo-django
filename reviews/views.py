from django.shortcuts import render, get_object_or_404, redirect
from .models import Review
from bookings.models import Booking
from django.contrib.auth.decorators import login_required

from .forms import ReviewForm

@login_required
def ReviewAddView(request, pk):
    booking = get_object_or_404(Booking, id=pk)
    print(booking.reviews.all()) 
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            # Simpan review
            Review.objects.create(
                user=request.user,
                bus=booking.bus,
                booking=booking,
                rating=form.cleaned_data['rating'],
                comment=form.cleaned_data['comment']
            )

            return redirect('bookings:booking_list')
    else:
        form = ReviewForm()

    return render(request, 'reviews/add_review.html', {'booking': booking, 'form':form})
