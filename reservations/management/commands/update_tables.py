from datetime import timedelta, date, time, datetime

import pytz
from dateutil.relativedelta import relativedelta
from django.core.management import BaseCommand

from reservations.models import Table


class Command(BaseCommand):
    """
     Находит просроченные столы и
     обновляет дату и доступность на следующий день.
    """

    def handle(self, *args, **options):
        numbers_table = Table.objects.all()
        for table in numbers_table:
            if datetime.now().timestamp() > table.datetime.timestamp():
                Table.objects.filter(id=table.id).update(
                    datetime=table.datetime + timedelta(days=1),
                    available=True,
                )
