from django.urls import path
from . import views

urlpatterns = [
    path('<int:booking_id>/', views.PaymentFormView.as_view(), name='payment_form'),  # Form Pembayaran
]
