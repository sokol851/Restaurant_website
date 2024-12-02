from datetime import datetime, timedelta
from django.core.management import BaseCommand
from django.utils import timezone

from reservations.models import Table
from restaurant.models import Restaurant


class Command(BaseCommand):
    """
    Создаём доступные столы
    """

    def handle(self, *args, **options):
        year_now = timezone.localtime(timezone.now()).year
        month_now = timezone.localtime(timezone.now()).month
        day_now = timezone.localtime(timezone.now()).day

        # Время столов
        datetime_objs = [
            timezone.make_aware(datetime(year_now, month_now, day_now, hour=10)),
            timezone.make_aware(datetime(year_now, month_now, day_now, hour=12)),
            timezone.make_aware(datetime(year_now, month_now, day_now, hour=14)),
            timezone.make_aware(datetime(year_now, month_now, day_now, hour=16)),
            timezone.make_aware(datetime(year_now, month_now, day_now, hour=18)),
            timezone.make_aware(datetime(year_now, month_now, day_now, hour=20)),
            timezone.make_aware(datetime(year_now, month_now, day_now, hour=22)),
        ]

        # Получаем рестораны
        cities = Restaurant.objects.all()

        # Создаём столы
        for city in cities:
            for number in range(1, city.tables_count + 1):
                for datetime_obj in datetime_objs:
                    table = Table.objects.create(
                        number=number,
                        is_datetime=datetime_obj,
                        restaurant=city
                    )
                    table.save()

        # Сразу проверяем просроченные столы
        numbers_table = Table.objects.all()
        for table in numbers_table:
            if datetime.now().timestamp() > table.is_datetime.timestamp():
                Table.objects.filter(id=table.id).update(
                    is_datetime=table.is_datetime + timedelta(days=1),
                    available=True,
                )
