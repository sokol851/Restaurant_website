from django.apps import AppConfig


class ReservationsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "reservations"
    verbose_name = "Бронирования"

    def ready(self):
        from . import signals
