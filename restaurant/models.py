from datetime import date

from dateutil.relativedelta import relativedelta
from django.db import models

from users.models import NULLABLE


def upload(self, filename):
    """ Функция для загрузки медиа по именам персонала """
    return 'staff/%s %s/%s' % (self.last_name, self.first_name, filename)


def upload_for_bg(self, filename):
    """ Функция для загрузки медиа в bg """
    return 'bg/%s' % (filename,)


def upload_for_restaurant(self, filename):
    """ Функция для загрузки схем в restaurant """
    return 'restaurant/%s' % (filename,)


class Restaurant(models.Model):
    """
    Модель ресторанов

    атрибуты:
        name (CharField): название ресторана
        city (CharField): город расположения
        tables_count (SmallIntegerField): количество столов
        scheme_tables (ImageField): фото схемы столов
        street улица (CharField):
        house_number (CharField): номер дома
        extra (CharField): дополнительная информация
        phone (CharField): номер телефона
        is_published (BooleanField): признак публикации
    """
    name = models.CharField(
        max_length=150,
        verbose_name='Название'
    )
    city = models.CharField(
        max_length=150,
        verbose_name='Город'
    )
    tables_count = models.SmallIntegerField(
        verbose_name='Количество столов',
        default=10
    )
    scheme_tables = models.ImageField(
        upload_to=upload_for_restaurant,
        **NULLABLE,
        verbose_name='Фото'
    )

    street = models.CharField(
        max_length=50,
        verbose_name='Улица', **NULLABLE
    )
    house_number = models.CharField(
        max_length=10,
        verbose_name='Номер дома', **NULLABLE
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
        verbose_name = 'Ресторан'
        verbose_name_plural = 'Рестораны'

    def __str__(self):
        return f'{self.name} - {self.city}'


class StaffRestaurant(models.Model):
    """
        Модель персонала

        атрибуты:
            first_name (CharField): имя сотрудника
            last_name (CharField): фамилия сотрудника
            photo (ImageField): фото сотрудника
            position (CharField): должность
            date_employment (DateField): дата трудоустройства
            is_published (BooleanField): публикация

        методы:
            experience - считает стаж сотрудника
            naming_day - определяет окончания дней
            naming_month - определяет окончания месяцев
            naming_year - определяет окончания лет
    """

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
        """ Определяет стаж сотрудника """
        return relativedelta(date.today(), self.date_employment)

    @property
    def naming_day(self):
        """ Определяет окончания дней """
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
        """ Определяет окончания месяцев """
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
        """ Определяет окончания лет """
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
    """
    Модель миссий ресторана

    атрибуты:
        mission (CharField): название миссии
        description (TextField): описание миссии
        serial_number (SmallIntegerField): порядковый номер
    """
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
    """
    Модель истории ресторана

    атрибуты:
        year (SmallIntegerField): год события
        activity (TextField): событие
    """
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
    """
    Модель баннера ресторана

    атрибуты:
        description (TextField): описание ресторана
        background (ImageField): фон для баннера
        is_published (BooleanField): признак публикации
    """
    description = models.TextField(
        verbose_name='Описание ресторана',
        **NULLABLE
    )
    background = models.ImageField(
        upload_to=upload_for_bg,
        verbose_name="Фон",
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
    """
    Модель услуг ресторана

    атрибуты:
        service (CharField): услуга ресторана
        is_published (BooleanField): признак публикации
    """
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
