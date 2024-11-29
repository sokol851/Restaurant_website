from django.db import models


class Table(models.Model):
    RESTAURANTS = {
        "SPB": "Saint-Petersburg",
        "MSK": "Moscow",
    }

    number = models.SmallIntegerField(
        verbose_name='Номер столика'
    )
    date = models.DateField(
        verbose_name='Дата'
    )
    time = models.TimeField(
        verbose_name='Время'
    )
    restaurant = models.CharField(
        max_length=10,
        choices=RESTAURANTS,
        verbose_name='Ресторан'
    )
    available = models.BooleanField(
        default=True,
        verbose_name='Доступен'
    )

    class Meta:
        verbose_name = 'Столик'
        verbose_name_plural = 'Столики'

    def __str__(self):
        return (f'{self.restaurant} - Стол №{self.number}'
                f' ({self.date.strftime("%d.%m.%Y")} - '
                f'{self.time.strftime("%H:%M")})')
