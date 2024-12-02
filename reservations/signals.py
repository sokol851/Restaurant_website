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
        HistoryReservations.objects.create(
            user=instance.user,
            create_at=timezone.localtime(timezone.now()),
            status=f'Ожидаем подтверждения брони - '
                   f'({Table.objects.get(id=instance.table.id)})',
        )
        # Делаем стол не доступным
        Table.objects.filter(id=instance.table.id).update(available=False)

    #  Если объект уже создан
    if not created:
        # Старый стол стал доступен
        Table.objects.filter(id=instance.old_table).update(available=True)
        # Новый стол - не доступен
        Table.objects.filter(id=instance.table.id).update(available=False)

        #  Обновляем значение поля old_table.
        (Reservation.objects.filter(id=instance.id).
         update(old_table=instance.table.id))

        #  Запись в историю об изменениях.
        if Table.objects.get(id=instance.old_table) != instance.table:
            HistoryReservations.objects.create(
                status=f'Бронь ({Table.objects.get(id=instance.old_table)})'
                       f' изменена на ({str(instance.table)})',
                user=instance.user,
                create_at=timezone.localtime(timezone.now())
            )


@receiver(post_delete, sender=Reservation)
def toggle_available_delete(sender, instance: Reservation, **kwargs):

    #  Стол становится доступным
    Table.objects.filter(id=instance.table.id).update(available=True)

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
        # print(stripe.Refund.create(charge=instance.session_id))
