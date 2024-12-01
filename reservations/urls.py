from reservations.apps import ReservationsConfig
from django.urls import path

from reservations.views import ReservationListView, ReservationUpdateView, ReservationCreateView, ReservationDeleteView

app_name = ReservationsConfig.name

urlpatterns = [
    path("reservations/", ReservationListView.as_view(), name="list_reservations"),
    path('reservations/<int:pk>/update', ReservationUpdateView.as_view(), name='update_reservations'),
    path('reservations/create/', ReservationCreateView.as_view(), name='create_reservations'),
    path('reservations/<int:pk>/delete', ReservationDeleteView.as_view(), name='delete_reservations'),
]
