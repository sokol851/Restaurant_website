import stripe
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone

from reservations.models import (
    Reservation,
    Table,
    HistoryReservations
)
from reservations.services import (
    create_product,
    create_price,
    create_session
)
from reservations.tasks import create_history, table_available, update_param


@receiver(post_save, sender=Reservation)
def toggle_available(sender, instance, created, **kwargs):
    #  Если ещё не создан
    if created:
        # Создаём продукт
        stripe_product = create_product(product=instance)
        # Создаём цену
        stripe_price = create_price(stripe_product, instance.amount)
        # Создаём сессию и ссылку
        session_id, payment_link = create_session(stripe_price)

        # Присваиваем значения
        Reservation.objects.filter(id=instance.id).update(
            old_table=instance.table.id,
            session_id=session_id,
            link=payment_link, )

        # Запись в историю о создании брони.
        create_history.delay(instance.id,
                             f'Ожидаем подтверждения брони -'
                             f' {Table.objects.get(id=instance.table.id)})')

        # Делаем стол не доступным
        table_available.delay(instance.table.id, False)

    # Если объект уже создан
    if not created:
        # Старый стол стал доступен
        table_available.delay(instance.old_table, True)

        # Новый стол - не доступен
        table_available.delay(instance.table.id, False)

        #  Обновляем значение поля old_table.
        update_param.delay(instance.id, instance.table.id)

        #  Запись в историю об изменениях.
        if Table.objects.get(id=instance.old_table) != instance.table:
            create_history.delay(
                instance.id,
                f'Бронь ({Table.objects.get(id=instance.old_table)})'
                f' изменена на ({str(instance.table)})')


@receiver(post_delete, sender=Reservation)
def toggle_available_delete(sender, instance, **kwargs):
    #  Стол становится доступным
    table_available.delay(instance.table.id, True)

    # Делаем запись в историю
    HistoryReservations.objects.create(
        status=f'Бронь ({str(instance.table)}) удалена!',
        user=instance.user,
        create_at=timezone.localtime(timezone.now())
    )

    # Оформляем возврат, если была оплата и время события не наступило.
    if ((stripe.checkout.Session.retrieve(instance.session_id).
                 payment_status == "paid")
            and timezone.localtime(timezone.now()).timestamp() <
            instance.table.is_datetime.timestamp()):
        print('Оформлен возврат депозита на карту')

        # Делаем запись в историю
        HistoryReservations.objects.create(
            status=f'Оформлен возврат депозита за бронь -'
                   f' ({str(instance.table)})!',
            user=instance.user,
            create_at=timezone.localtime(timezone.now())
        )
        # print(stripe.Refund.create(charge=instance.session_id))
