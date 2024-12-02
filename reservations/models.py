from datetime import datetime, timedelta

import stripe
from django.conf import settings
from django.db import models

from reservations.services import get_status_session
from reservations.validators import check_amount, phone_number
from restaurant.models import Restaurant
from users.models import NULLABLE


class Table(models.Model):
    number = models.SmallIntegerField(
        verbose_name='Номер столика'
    )
    is_datetime = models.DateTimeField(
        verbose_name='Время',
        **NULLABLE
    )
    restaurant = models.ForeignKey(
        Restaurant,
        verbose_name='Ресторан',
        on_delete=models.CASCADE
    )
    places = models.CharField(
        max_length=30,
        **NULLABLE,
        verbose_name='Вместимость'
    )
    available = models.BooleanField(
        default=True,
        verbose_name='Доступность'
    )

    class Meta:
        verbose_name = 'Столик'
        verbose_name_plural = 'Столики'
        ordering = ['restaurant', 'number', 'is_datetime']

    def __str__(self):
        return (f'{self.restaurant} - Стол №{self.number}'
                f' {self.is_datetime.date()} '
                f'{(self.is_datetime + timedelta(hours=3)).time()}')


class Reservation(models.Model):
    table = models.ForeignKey(
        Table,
        on_delete=models.CASCADE,
        verbose_name='Стол'
    )
    old_table = models.IntegerField(
        verbose_name='id предыдущего стола',
        **NULLABLE
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        **NULLABLE
    )
    phone = models.CharField(
        max_length=20,
        verbose_name="Телефон",
        validators=[phone_number]
    )
    comment = models.TextField(
        **NULLABLE,
        verbose_name="Комментарий"
    )
    amount = models.IntegerField(
        default=500,
        verbose_name='Депозит',
        validators=[check_amount]
    )
    create_at = models.DateTimeField(
        default=datetime.today(),
        verbose_name='Время создания'
    )
    is_confirmed = models.BooleanField(
        default=False,
        verbose_name='Подтвержденная бронь'
    )
    session_id = models.CharField(
        max_length=150,
        verbose_name='Сессия',
        **NULLABLE
    )
    link = models.URLField(
        max_length=500,
        verbose_name='Cсылка на оплату',
        **NULLABLE
    )

    class Meta:
        verbose_name = 'Бронь'
        verbose_name_plural = 'Брони'

    def __str__(self):
        return f'{self.user} - {self.table}'


class HistoryReservations(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        **NULLABLE
    )
    create_at = models.DateTimeField(
        default=datetime.today(),
        verbose_name='Время создания'
    )
    status = models.CharField(
        max_length=150,
        default='Ожидаем вас',
        verbose_name='статус',
        **NULLABLE
    )

    class Meta:
        verbose_name = 'История резервирования'
        verbose_name_plural = 'История резервирования'
        ordering = ['-create_at']

    def __str__(self):
        return self.status
