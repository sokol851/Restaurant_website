from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from reservations.models import Reservation


@receiver(post_save, sender=Reservation)
def toggle_available(sender, instance: Reservation, created, **kwargs):
    if not created:
        if instance.is_confirmed is True:
            instance.table.available = False
            instance.table.save()


@receiver(post_delete, sender=Reservation)
def toggle_available(sender, instance: Reservation, **kwargs):
    instance.table.available = True
    instance.table.save()
