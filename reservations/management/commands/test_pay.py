from datetime import timedelta, datetime

from django.core.management import BaseCommand

from reservations.models import Reservation
from reservations.services import get_status_session


class Command(BaseCommand):
    """
     Находит просроченные столы и
     обновляет дату и доступность на следующий день.
    """

    def handle(self, *args, **options):
        reservation = Reservation.objects.all()
        for i in reservation:
            payment = get_status_session(i.session_id)
            if payment.payment_status == 'paid':
                i.is_confirmed = True
                i.save()
