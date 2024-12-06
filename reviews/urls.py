from django.urls import path
from . import views

urlpatterns = [
    path('', views.ReviewListView.as_view(), name='review_list'),  # Daftar Review
    # path('add/<int:bus_id>/', views.AddReviewView.as_view(), name='add_review'),  # Tambah Review
    path('detail/<int:bus_id>/', views.ReviewDetailView.as_view(), name="review_detail")
]
