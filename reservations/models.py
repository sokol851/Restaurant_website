from datetime import datetime, timedelta
from django.conf import settings
from django.db import models

from users.models import NULLABLE

from django.dispatch import receiver
from django.db.models.signals import post_save


class Table(models.Model):
    RESTAURANTS = {
        "SPB": "Saint-Petersburg",
        "MSK": "Moscow",
    }

    number = models.SmallIntegerField(
        verbose_name='Номер столика'
    )
    datetime = models.DateTimeField(
        verbose_name='Время',
        **NULLABLE
    )
    restaurant = models.CharField(
        max_length=10,
        choices=RESTAURANTS,
        verbose_name='Ресторан'
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

    def __str__(self):
        return (f'{self.restaurant} - Стол №{self.number}'
                f' {self.datetime.date()} '
                f'{(self.datetime + timedelta(hours=3)).time()}')


class Reservation(models.Model):
    table = models.ForeignKey(
        Table,
        on_delete=models.CASCADE,
        verbose_name='Стол'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    phone = models.CharField(
        max_length=20,
        verbose_name="Телефон"
    )
    comment = models.TextField(
        **NULLABLE,
        verbose_name="Комментарий"
    )
    amount = models.IntegerField(
        default=500,
        verbose_name='Депозит'
    )
    create_at = models.DateTimeField(
        default=datetime.today(),
        verbose_name='Время создания'
    )
    is_confirmed = models.BooleanField(
        default=False,
        verbose_name='Подтвержденная бронь'
    )

    class Meta:
        verbose_name = 'Бронь'
        verbose_name_plural = 'Брони'

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} - {self.table}'
