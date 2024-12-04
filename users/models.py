import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {"blank": True, "null": True}


def upload_for_users(self, filename):
    """ Функция для загрузки медиа пользователей по их email """
    return 'users/%s/%s' % (self.email, filename)


class User(AbstractUser):
    """
    Модель пользователя

    Атрибуты:
        username (None): ник
        email (EmailField): почта
        phone (CharField): телефон
        first_name (CharField): имя
        last_name (CharField): фамилия
        avatar (ImageField): аватар
        is_active (BooleanField): активация
        token_verify (UUIDField): токен для регистрации
    """

    username = None

    email = models.EmailField(
        unique=True,
        verbose_name="Почта"
    )

    phone = models.CharField(
        max_length=35,
        verbose_name="Телефон",
        **NULLABLE,
        default="Не указано"
    )

    first_name = models.CharField(
        max_length=150,
        default="Не указано",
        verbose_name="Имя",
        **NULLABLE
    )

    last_name = models.CharField(
        max_length=150,
        default="Не указано",
        verbose_name="Фамилия",
        **NULLABLE
    )

    avatar = models.ImageField(
        upload_to=upload_for_users,
        default="non_avatar.png",
        verbose_name="Аватар",
        **NULLABLE
    )

    is_active = models.BooleanField(
        default=False
    )

    token_verify = models.UUIDField(
        default=uuid.uuid4,
        unique=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
