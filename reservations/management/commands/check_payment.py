from datetime import datetime

from django.core.management import BaseCommand

from reservations.models import Reservation, HistoryReservations
from reservations.services import get_status_session


class Command(BaseCommand):
    """
     Проверяет статус оплаты и меняет статус подтверждения брони.
    """

    def handle(self, *args, **options):
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
                        create_at=datetime.now()
                    )
                    i.is_confirmed = True
                    i.save()
