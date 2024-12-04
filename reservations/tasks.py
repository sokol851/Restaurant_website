from celery import shared_task
from config.celery import app


@shared_task
def update_reservations():
    """ Отправка задачи обновления резервирований в планировщик """

    from django.core import management
    # Обновление доступных столов
    management.call_command('update_tables')
    # Проверка оплат для подтверждения брони
    management.call_command('check_payment')
    # Удаление не оплаченных броней по истечении 30 минут
    management.call_command('check_confirm')


@app.task
def create_history(id_reservation, status):
    """ Задача создания записи в истории """

    from reservations.models import HistoryReservations
    from django.utils import timezone
    from reservations.models import Reservation

    instance = Reservation.objects.get(id=id_reservation)
    HistoryReservations.objects.create(
        user=instance.user,
        create_at=timezone.localtime(timezone.now()),
        status=status
    )


@app.task
def table_available(table_id, value):
    """ Задача переключения доступности столика. """

    from reservations.models import Table
    Table.objects.filter(id=table_id).update(available=value)


@app.task
def update_param(id_reservation, value):
    """ Задача обновления поля номера старого стола """

    from reservations.models import Reservation
    Reservation.objects.filter(id=id_reservation).update(old_table=value)
