from datetime import timedelta, datetime

from django.core.management import BaseCommand

from reservations.models import Table, Reservation, HistoryReservations


class Command(BaseCommand):
    """
     Находит просроченные столы и
     обновляет дату и доступность на следующий день.
    """

    def handle(self, *args, **options):
        numbers_table = Table.objects.all()
        reservations = Reservation.objects.all()
        for table in numbers_table:
            # Если время прошло - перемещаем стол на день вперёд.
            if datetime.now().timestamp() > table.is_datetime.timestamp():
                Table.objects.filter(id=table.id).update(
                    is_datetime=table.is_datetime + timedelta(days=1),
                    available=True,
                )

                # Проверяем существующие резервы и завершаем просроченные.
                for reservation in reservations:
                    if table == reservation.table:
                        # Создаём запись в историю об этом.
                        HistoryReservations.objects.create(
                            status=f'Событие ({reservation.table}) завершено!',
                            user=reservation.user,
                            create_at=datetime.now()
                        )
                        reservation.delete()
