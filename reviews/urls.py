from django.urls import path
from . import views

app_name = "reviews"

urlpatterns = [
    path('<int:pk>/', views.ReviewAddView, name="review_add")
]
