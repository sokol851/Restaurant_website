from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        """
        Находит просроченные столы и
        обновляет дату и доступность на следующий день.
        """
        from datetime import timedelta
        from django.utils import timezone
        from reservations.models import Table, Reservation, HistoryReservations

        numbers_table = Table.objects.all()
        reservations = Reservation.objects.all()
        for table in numbers_table:

            # Если время прошло - перемещаем стол на день вперёд.
            if (timezone.localtime(timezone.now()).timestamp() >
                    timezone.localtime(table.is_datetime).timestamp()):
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
                            create_at=timezone.localtime(timezone.now())
                        )
                        reservation.delete()
