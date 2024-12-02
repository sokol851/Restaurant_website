from django.core.management import BaseCommand


class Command(BaseCommand):
    """
    Создаём доступные столы
    """

    def handle(self, *args, **options):
        from django.utils import timezone
        from datetime import datetime, timedelta
        from reservations.models import Table
        from restaurant.models import Restaurant

        year_now = timezone.localtime(timezone.now()).year
        month_now = timezone.localtime(timezone.now()).month
        day_now = timezone.localtime(timezone.now()).day

        # Время столов
        hours = [10, 12, 14, 16, 18, 20, 22]

        # Получаем рестораны
        cities = Restaurant.objects.all()

        # Создаём столы
        for city in cities:
            for number in range(1, city.tables_count + 1):
                for hour in hours:

                    # Создаём экземпляр времени
                    datetime_obj = timezone.make_aware(datetime(year_now,
                                                                month_now,
                                                                day_now,
                                                                hour=hour))
                    # Проверяем, что стол не создан
                    if not Table.objects.filter(number=number,
                                                is_datetime=datetime_obj,
                                                restaurant=city):
                        # Создаём стол
                        table = Table.objects.create(number=number,
                                                     is_datetime=datetime_obj,
                                                     restaurant=city)
                        table.save()

        # Сразу проверяем просроченные столы
        numbers_table = Table.objects.all()
        for table in numbers_table:
            if datetime.now().timestamp() > table.is_datetime.timestamp():
                Table.objects.filter(id=table.id).update(
                    is_datetime=table.is_datetime + timedelta(days=1),
                    available=True,
                )
