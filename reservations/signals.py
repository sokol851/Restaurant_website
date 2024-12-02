from datetime import datetime

import stripe
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from reservations.models import Reservation, Table, HistoryReservations


@receiver(post_save, sender=Reservation)
def toggle_available(sender, instance, created, **kwargs):

    if created:
        (Reservation.objects.filter(id=instance.id).
         update(old_table=instance.table.id))

        HistoryReservations.objects.create(
            user=instance.user,
            create_at=datetime.now(),
            status=f'Ожидаем вас в ({Table.objects.get(id=instance.table.id)})',
        )
        if instance.is_confirmed:
            Table.objects.filter(id=instance.table.id).update(available=False)

    if not created:
        if instance.is_confirmed is True:
            Table.objects.filter(id=instance.old_table).update(available=True)
            Table.objects.filter(id=instance.table.id).update(available=False)

            (Reservation.objects.filter(id=instance.id).
             update(old_table=instance.table.id))

            HistoryReservations.objects.create(
                status=f'Бронь ({Table.objects.get(id=instance.old_table)})'
                       f' изменена на ({str(instance.table)})',
                user=instance.user,
                create_at=datetime.now()
            )

        else:
            Table.objects.filter(id=instance.old_table).update(available=True)
            Table.objects.filter(id=instance.table.id).update(available=True)

            (Reservation.objects.filter(id=instance.id).
             update(old_table=instance.table.id))

            HistoryReservations.objects.create(
                status=f'Бронь ({Table.objects.get(id=instance.old_table)})'
                       f' изменена на ({str(instance.table)})',
                user=instance.user,
                create_at=datetime.now()
            )


@receiver(post_delete, sender=Reservation)
def toggle_available(sender, instance: Reservation, **kwargs):
    Table.objects.filter(id=instance.table.id).update(available=True)
    HistoryReservations.objects.create(
        status=f'Бронь ({str(instance.table)}) удалена!',
        user=instance.user,
        create_at=datetime.now()
    )

    # if stripe.checkout.Session.retrieve(instance.session_id).payment_status == "paid":
    #     print('Оформлен возврат депозита на карту')
    #     stripe.Refund.create(charge=self.session_id)
