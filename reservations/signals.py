from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from reservations.models import Reservation, Table


@receiver(post_save, sender=Reservation)
def toggle_available(sender, instance, created, **kwargs):
    if created:
        Reservation.objects.filter(id=instance.id).update(old_table=instance.table.id)
    if not created:
        if instance.is_confirmed is True:
            Table.objects.filter(id=instance.old_table).update(available=True)
            Table.objects.filter(id=instance.table.id).update(available=False)
            Reservation.objects.filter(id=instance.id).update(old_table=instance.table.id)
        else:
            Table.objects.filter(id=instance.old_table).update(available=True)
            Table.objects.filter(id=instance.table.id).update(available=True)
            Reservation.objects.filter(id=instance.id).update(old_table=instance.table.id)


@receiver(post_delete, sender=Reservation)
def toggle_available(sender, instance: Reservation, **kwargs):
    instance.table.available = True
    instance.table.save()
