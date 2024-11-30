from reservations.apps import ReservationsConfig
from django.urls import path

from reservations.views import ReservationListView, ReservationUpdateView

app_name = ReservationsConfig.name

urlpatterns = [
    path("reservations/", ReservationListView.as_view(), name="list_reservations"),
    path('reservations/<int:pk>', ReservationUpdateView.as_view(), name='update_reservations'),
]
