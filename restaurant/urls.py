from django.urls import path

from restaurant.apps import RestaurantConfig
from restaurant.views import AboutView, Index

app_name = RestaurantConfig.name

urlpatterns = [
    path("", Index.as_view(), name="index"),
    path("about/", AboutView.as_view(), name="about"),
]
