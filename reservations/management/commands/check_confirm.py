from datetime import datetime

from django.core.management import BaseCommand

from reservations.models import Reservation, HistoryReservations


class Command(BaseCommand):
    """
     Находит неоплаченные брони и удаляет их за 30 минут до начала события.
    """

    def handle(self, *args, **options):
        reservation = Reservation.objects.all()
        for i in reservation:
            delta = (datetime.now().timestamp() -
                     i.table.is_datetime.timestamp())
            if not i.is_confirmed:
                if delta > -1800:
                    # Создаём запись в историю об этом
                    HistoryReservations.objects.create(
                        status=f'Оплата брони ({i.table}) просрочена!',
                        user=i.user,
                        create_at=datetime.now())
                    # Удаляем
                    i.delete()
