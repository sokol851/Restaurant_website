from datetime import datetime
from django.core.management import BaseCommand

from reservations.models import Table


class Command(BaseCommand):
    """
    Создаём доступные столы
    """

    def handle(self, *args, **options):
        numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        year_now = datetime.now().year
        month_now = datetime.now().month
        day_now = datetime.now().day
        datetime_objs = [
            datetime(year_now, month_now, day_now, hour=10),
            datetime(year_now, month_now, day_now, hour=12),
            datetime(year_now, month_now, day_now, hour=14),
            datetime(year_now, month_now, day_now, hour=16),
            datetime(year_now, month_now, day_now, hour=18),
            datetime(year_now, month_now, day_now, hour=20),
            datetime(year_now, month_now, day_now, hour=22),
        ]

        cities = [
            'SPB',
            'MSK'
        ]

        for city in cities:
            for number in numbers:
                for datetime_obj in datetime_objs:
                    table = Table.objects.create(
                        number=number,
                        datetime=datetime_obj,
                        restaurant=city
                    )
                    table.save()
