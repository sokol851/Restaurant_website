import stripe
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.utils import timezone

from config import settings
from reservations.models import HistoryReservations, Reservation, Table
from reservations.services import create_price, create_product, create_session
from reservations.tasks import create_history, table_available, update_param
from restaurant.tasks import task_send_mail
from users.models import User


@receiver(post_save, sender=Reservation)
def toggle_available(sender, instance, created, **kwargs):
    """Сигнал для создания или изменения резервирования"""

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
            link=payment_link,
        )

        # Готовим уведомление о создании брони для почты
        is_date_time = timezone.localtime(instance.table.is_datetime).strftime(
            "%d.%m.%Y %H:%M"
        )
        restaurant = instance.table.restaurant

        subject = f'Бронь столика в ресторане "{restaurant}"'
        body = (
            f"Добрый день!\n\n"
            f"Вами зарезервирован столик в ресторане"
            f" '{restaurant}', время {is_date_time}.\n"
            f"Во избежание отмены - подтвердите резерв оплатой депозита"
            f" в течение 30 минут.\n\n"
            f"Оплата депозита по ссылке: {instance.link}"
        )
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [instance.user.email]

        # Отправляем задачу отправки письма в celery
        task_send_mail.delay(subject, body, from_email, recipient_list)

        # Запись в историю о создании брони.
        create_history.delay(
            instance.id,
            f"Ожидаем подтверждения брони -"
            f" {Table.objects.get(id=instance.table.id)})",
        )

        # Делаем стол не доступным
        table_available.delay(instance.table.id, False)

    # Если объект уже создан
    else:
        #  Запись в историю об изменениях.
        if Table.objects.get(id=instance.old_table) != instance.table:
            # Старый стол стал доступен
            table_available.delay(instance.old_table, True)

            # Новый стол - не доступен
            table_available.delay(instance.table.id, False)

            #  Обновляем значение поля old_table.
            update_param.delay(instance.id, instance.table.id)

            create_history.delay(
                instance.id,
                f"Бронь ({Table.objects.get(id=instance.old_table)})"
                f" изменена на ({str(instance.table)})",
            )

            # Собираем письмо
            user_email = User.objects.get(id=instance.user.id).email
            is_time = timezone.localtime(instance.table.is_datetime).strftime(
                "%d.%m.%Y %H:%M"
            )
            old_table = Table.objects.get(id=instance.old_table)
            old_table_time = (timezone.localtime(old_table.is_datetime).
                              strftime('%d.%m.%Y %H:%M'))

            subject = (f'Изменение столика в ресторане'
                       f' "{instance.table.restaurant}"')
            body = (f"Добрый день!\n\n"
                    f"Вы изменили бронь в ресторане"
                    f" '{instance.table.restaurant}', с '{old_table_time}'"
                    f" на время '{is_time}'.\n\n"
                    f"Проверьте изменения в личном кабинете: "
                    f"{settings.SITE_URL}/reservations/")
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [user_email]

            # Отправляем задачу отправки письма в celery
            task_send_mail.delay(subject, body, from_email, recipient_list)


@receiver(post_delete, sender=Reservation)
def toggle_available_delete(sender, instance, **kwargs):
    """Сигнал для удаления резервирования"""
    #  Стол становится доступным
    table_available.delay(instance.table.id, True)

    # Делаем запись в историю
    HistoryReservations.objects.create(
        status=f"Бронь ({str(instance.table)}) удалена!",
        user=instance.user,
        create_at=timezone.localtime(timezone.now()),
    )

    # Готовим уведомление о создании брони для почты
    is_date_time = timezone.localtime(instance.table.is_datetime).strftime(
        "%d.%m.%Y %H:%M"
    )
    restaurant = instance.table.restaurant

    subject = f'Бронь столика в ресторане "{restaurant} отменена!"'
    body = (
        f"Добрый день!\n\n"
        f"Бронь столика в ресторане"
        f" '{restaurant}', время {is_date_time} отменена.\n"
        f"Если вы оплатили бронь, но событие ещё не состоялось -"
        f" деньги вернутся на вашу карту."
    )
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [instance.user.email]

    # Отправляем задачу отправки письма в celery
    task_send_mail.delay(subject, body, from_email, recipient_list)

    # Оформляем возврат, если была оплата и время события не наступило.
    if instance.session_id:
        if (
                stripe.checkout.Session.retrieve(
                    instance.session_id).payment_status == "paid"
                and timezone.localtime(timezone.now()).timestamp()
                < instance.table.is_datetime.timestamp()
        ):
            # Делаем запись в историю
            HistoryReservations.objects.create(
                status=f"Оформлен возврат депозита за бронь -"
                       f" ({str(instance.table)})!",
                user=instance.user,
                create_at=timezone.localtime(timezone.now()),
            )

            print("Оформлен возврат депозита на карту")
            # Создаём возврат в Stripe если он был не тестовый.
            # stripe.Refund.create(charge=instance.session_id)
