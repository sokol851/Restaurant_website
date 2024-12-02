from celery import shared_task


@shared_task
def update_reservations():
    from django.core import management
    """ Отправка задачи обновления резервирований в планировщик """
    management.call_command('update_tables')
    management.call_command('check_payment')
    management.call_command('check_confirm')
