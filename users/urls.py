from django.urls import path
from . import views
from .views import RegisterView, CustomLoginView, CustomLogoutView, ProfileView, EditProfileView

app_name = 'users'

urlpatterns = [
    path('', views.home_view, name='homepage'),
    # path('register/', views.register_view, name='register'),
    # path('login/', views.login_view, name='login'),
    # path('logout/', views.logout_view, name='logout'),
    # path('profile/', views.profile_view, name='profile'),
    # path('profile/edit/', views.edit_profile_view, name='edit_profile'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/edit/', EditProfileView.as_view(), name='edit_profile'),
]