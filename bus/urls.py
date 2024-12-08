from django.urls import path
from . import views

app_name = 'bus'

urlpatterns = [
    path('list/', views.BusListView.as_view(), name='bus_list'),  
    path('add/', views.AddBusView.as_view(), name='bus_add'),  
    path('delete/<int:pk>/', views.DeleteBusView.as_view(), name='bus_delete'),  
    path('update/<int:pk>/', views.UpdateBusView.as_view(), name='bus_update'),  
    path('', views.BusListCustomerView.as_view(), name='bus_list_customer'),
    path('<int:pk>/', views.BusDetailCustomerView.as_view(), name='bus_detail_customer'),
]
