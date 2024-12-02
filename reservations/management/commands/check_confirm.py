from datetime import timedelta, datetime

from django.core.management import BaseCommand

from reservations.models import Reservation, HistoryReservations
from reservations.services import get_status_session


class Command(BaseCommand):
    """
     Находит неоплаченные брони и удаляет их за 2 часа до начала события.
    """

    def handle(self, *args, **options):
        reservation = Reservation.objects.all()
        for i in reservation:
            delta = (datetime.now().timestamp() -
                     i.table.is_datetime.timestamp())
            if not i.is_confirmed:
                if delta > -7200:
                    HistoryReservations.objects.create(
                        status=f'Оплата брони ({i.table}) просрочена!',
                        user=i.user,
                        create_at=datetime.now())
                    i.delete()
