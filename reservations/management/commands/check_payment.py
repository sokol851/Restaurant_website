from django.core.management import BaseCommand
from django.utils import timezone


class Command(BaseCommand):
    def handle(self, *args, **options):
        """
        Проверяет статус оплаты и меняет статус подтверждения брони.
        """
        import stripe
        from decouple import config

        from reservations.models import HistoryReservations, Reservation
        from reservations.services import get_status_session

        stripe.api_key = config("API_KEY_STRIPE")

        reservations = Reservation.objects.all()
        for reservation in reservations:
            # проверяем только не подтверждённые брони
            if not reservation.is_confirmed:
                payment = get_status_session(reservation.session_id)
                # Если сессия оплачена - подтверждаем бронь.
                if payment.payment_status == "paid":
                    if not reservation.is_confirmed:
                        # Создаём запись в историю об этом.
                        HistoryReservations.objects.create(
                            status=f"Бронь ({reservation.table}) подтверждена!",
                            user=reservation.user,
                            create_at=timezone.localtime(timezone.now()),
                        )
                        # Подтверждаем бронь
                        reservation.is_confirmed = True
                        reservation.save()
