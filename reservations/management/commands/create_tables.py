from datetime import datetime
from django.core.management import BaseCommand

from reservations.models import Table


class Command(BaseCommand):
    """
    Создаём доступные столы
    """
    def handle(self, *args, **options):
        numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        datetime_objs = [
            datetime(2024, 11, 29, 10),
            datetime(2024, 11, 29, 12),
            datetime(2024, 11, 29, 14),
            datetime(2024, 11, 29, 16),
            datetime(2024, 11, 29, 18),
            datetime(2024, 11, 29, 20),
            datetime(2024, 11, 29, 22),
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
