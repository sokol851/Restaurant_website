from datetime import date

from dateutil.relativedelta import relativedelta
from django.db import models

from users.models import NULLABLE


def upload(self, filename):
    return 'staff/%s %s/%s' % (self.last_name, self.first_name, filename)


class StaffRestaurant(models.Model):
    DAYS = ['дня', 'дней', 'день']
    MONTHS = ['месяца', 'месяцев', 'месяц']
    YEARS = ['года', 'лет', 'год']

    first_name = models.CharField(
        max_length=75,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=75,
        verbose_name='Фамилия'
    )
    photo = models.ImageField(
        upload_to=upload,
        default="non_avatar.png",
        **NULLABLE,
        verbose_name='Фото'
    )
    position = models.CharField(
        max_length=50,
        verbose_name='Должность'
    )
    date_employment = models.DateField(
        verbose_name="Дата трудоустройства",
        **NULLABLE)
    is_published = models.BooleanField(
        default=True,
        verbose_name='Публикация'
    )

    @property
    def experience(self):
        return relativedelta(date.today(), self.date_employment)

    @property
    def naming_day(self):
        name_day = None
        if self.experience.days % 10 == 1:
            name_day = self.DAYS[2]
        if self.experience.days % 10 in [2, 3, 4]:
            name_day = self.DAYS[0]
        if self.experience.days % 10 in [0, 5, 6, 7, 8, 9]:
            name_day = self.DAYS[1]
        return name_day

    @property
    def naming_month(self):
        name_month = None
        if self.experience.months % 10 == 1:
            name_month = self.MONTHS[2]
        if self.experience.months % 10 in [2, 3, 4]:
            name_month = self.MONTHS[0]
        if self.experience.months % 10 in [0, 5, 6, 7, 8, 9]:
            name_month = self.MONTHS[1]
        return name_month

    @property
    def naming_year(self):
        name_year = None
        if self.experience.years % 10 == 1:
            name_year = self.YEARS[2]
        if self.experience.years % 10 in [2, 3, 4]:
            name_year = self.YEARS[0]
        if (self.experience.years % 10 in [0, 5, 6, 7, 8, 9]
                or self.experience.years % 100 in [11, 12, 13, 14]):
            name_year = self.YEARS[1]
        return name_year

    class Meta:
        verbose_name = 'Персонал'
        verbose_name_plural = 'Персонал'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class MissionsRestaurant(models.Model):
    mission = models.CharField(
        max_length=50,
        verbose_name='Миссия'
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    serial_number = models.SmallIntegerField(
        verbose_name='Порядковый номер',
        **NULLABLE
    )

    class Meta:
        verbose_name = 'Миссия'
        verbose_name_plural = 'Миссии'

    def __str__(self):
        return self.mission


class HistoryRestaurant(models.Model):
    year = models.SmallIntegerField(
        verbose_name='Год'
    )
    activity = models.TextField(
        verbose_name='Событие'
    )

    class Meta:
        verbose_name = 'История'
        verbose_name_plural = 'Истории'

    def __str__(self):
        return self.activity


class Description(models.Model):
    description = models.TextField(
        verbose_name='Описание ресторана'
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name='Признак публикации'
    )

    class Meta:
        verbose_name = 'Описание ресторана'
        verbose_name_plural = 'Описания ресторана'

    def __str__(self):
        return self.description


class Services(models.Model):
    service = models.CharField(
        max_length=100,
        verbose_name='Услуга ресторана'
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name='Признак публикации'
    )

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'

    def __str__(self):
        return self.service


class Contacts(models.Model):
    city = models.CharField(
        max_length=50,
        verbose_name='Город'
    )
    street = models.CharField(
        max_length=50,
        verbose_name='Улица'
    )
    house_number = models.CharField(
        max_length=10,
        verbose_name='Номер дома'
    )
    extra = models.CharField(
        max_length=100,
        verbose_name='Дополнительная информация',
        **NULLABLE
    )
    phone = models.CharField(
        max_length=15,
        verbose_name='Номер телефона',
        **NULLABLE
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name='Признак публикации'
    )

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'

    def __str__(self):
        return f"{self.city} ({self.street}) - {self.phone}"
