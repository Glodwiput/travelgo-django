from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
    path('', views.ServiceListView.as_view(), name='service_list'),  
    path('add/', views.AddServiceView.as_view(), name='service_add'),  
    path('delete/<int:pk>/', views.DeleteServiceView.as_view(), name='service_delete'),  
    path('update/<int:pk>/', views.UpdateServiceView.as_view(), name='service_update'),  
]
