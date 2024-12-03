from django.core.management import BaseCommand
from django.utils import timezone


class Command(BaseCommand):
    """
     Проверяет статус оплаты и меняет статус подтверждения брони.
    """

    def handle(self, *args, **options):
        from datetime import datetime
        from reservations.models import Reservation, HistoryReservations
        from reservations.services import get_status_session
        import stripe
        from decouple import config

        stripe.api_key = config('API_KEY_STRIPE')

        reservation = Reservation.objects.all()
        for i in reservation:
            payment = get_status_session(i.session_id)

            # Если сессия оплачена - подтверждаем бронь.
            if payment.payment_status == 'paid':
                if not i.is_confirmed:
                    # Создаём запись в историю об этом.
                    HistoryReservations.objects.create(
                        status=f'Бронь ({i.table}) подтверждена!',
                        user=i.user,
                        create_at=timezone.localtime(timezone.now())
                    )
                    i.is_confirmed = True
                    i.save()
