from django.views.generic import ListView
from django.views.generic import DetailView
from .models import Review

class ReviewListView(ListView):
    model = Review
    template_name = 'reviews/review_list.html'


class ReviewDetailView(DetailView):
    model = Review
    template_name = 'reviews/review_detail.html'
