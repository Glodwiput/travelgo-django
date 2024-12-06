from django.urls import path
from . import views

urlpatterns = [
    path('', views.BusListView.as_view(), name='bus_list'),  # Daftar Bus
    path('<int:pk>/', views.BusDetailView.as_view(), name='bus_detail'),  # Detail Bus
]
