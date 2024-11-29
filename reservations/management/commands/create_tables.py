from datetime import time, date

from django.core.management import BaseCommand

from reservations.models import Table


class Command(BaseCommand):

    def handle(self, *args, **options):
        numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        times = [
            time(10, 00, 00),
            time(12, 00, 00),
            time(14, 00, 00),
            time(16, 00, 00),
            time(18, 00, 00),
            time(20, 00, 00),
            time(22, 00, 00),
        ]

        date_obj = date.today()

        cities = [
            'SPB',
            'MSK'
        ]
        for city in cities:
            for number in numbers:
                for time_obj in times:
                    table = Table.objects.create(
                        number=number,
                        time=time_obj,
                        date=date_obj,
                        restaurant=city
                    )
                    table.save()
