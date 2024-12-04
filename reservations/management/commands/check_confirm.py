from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        """
        Находит неоплаченные брони и удаляет их за 30 минут до начала события.
        """
        from django.utils import timezone
        from reservations.models import Reservation, HistoryReservations

        reservations = Reservation.objects.all()

        for reservation in reservations:
            reservation_time = reservation.create_at.timestamp()
            now_time = timezone.localtime(timezone.now()).timestamp()
            delta = now_time - reservation_time

            # Если прошло больше 30 минут без оплаты - бронь снимается
            if not reservation.is_confirmed:
                if delta > 1800:
                    # Создаём запись в историю об этом
                    HistoryReservations.objects.create(
                        status=f"Оплата брони ({reservation.table})"
                               f" просрочена!",
                        user=reservation.user,
                        create_at=timezone.localtime(timezone.now()),
                    )
                    # Удаляем
                    reservation.delete()
