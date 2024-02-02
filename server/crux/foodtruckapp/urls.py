from django.urls import path
from .views import FoodTruckView

urlpatterns = [
    path("foodtruck/", FoodTruckView.as_view()),
]
