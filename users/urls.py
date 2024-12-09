from django.urls import path
from . import views
from .views import RegisterView, CustomLoginView, CustomLogoutView, UserListView, UserAddView, UserDeleteView, reports_view

app_name = 'users'

urlpatterns = [
    path('', views.home_view, name='homepage'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),

    path('user/', UserListView.as_view(), name='user_list'),
    path('user/add/', UserAddView.as_view(), name='user_add'),
    path('user/delete/<int:pk>', UserDeleteView.as_view(), name='user_delete'),
    path('reports/', reports_view, name='reports'),
]