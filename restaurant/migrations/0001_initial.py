# Generated by Django 5.1.3 on 2024-12-02 23:03

import restaurant.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Contacts",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("city", models.CharField(max_length=50, verbose_name="Город")),
                ("street", models.CharField(max_length=50, verbose_name="Улица")),
                (
                    "house_number",
                    models.CharField(max_length=10, verbose_name="Номер дома"),
                ),
                (
                    "extra",
                    models.CharField(
                        blank=True,
                        max_length=100,
                        null=True,
                        verbose_name="Дополнительная информация",
                    ),
                ),
                (
                    "phone",
                    models.CharField(
                        blank=True,
                        max_length=15,
                        null=True,
                        verbose_name="Номер телефона",
                    ),
                ),
                (
                    "is_published",
                    models.BooleanField(
                        default=True, verbose_name="Признак публикации"
                    ),
                ),
            ],
            options={
                "verbose_name": "Контакт",
                "verbose_name_plural": "Контакты",
            },
        ),
        migrations.CreateModel(
            name="Description",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True, null=True, verbose_name="Описание ресторана"
                    ),
                ),
                (
                    "background",
                    models.ImageField(
                        upload_to=restaurant.models.upload_for_bg, verbose_name="Фон"
                    ),
                ),
                (
                    "is_published",
                    models.BooleanField(
                        default=True, verbose_name="Признак публикации"
                    ),
                ),
            ],
            options={
                "verbose_name": "Описание ресторана",
                "verbose_name_plural": "Описания ресторана",
            },
        ),
        migrations.CreateModel(
            name="HistoryRestaurant",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("year", models.SmallIntegerField(verbose_name="Год")),
                ("activity", models.TextField(verbose_name="Событие")),
            ],
            options={
                "verbose_name": "История",
                "verbose_name_plural": "Истории",
            },
        ),
        migrations.CreateModel(
            name="MissionsRestaurant",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("mission", models.CharField(max_length=50, verbose_name="Миссия")),
                ("description", models.TextField(verbose_name="Описание")),
                (
                    "serial_number",
                    models.SmallIntegerField(
                        blank=True, null=True, verbose_name="Порядковый номер"
                    ),
                ),
            ],
            options={
                "verbose_name": "Миссия",
                "verbose_name_plural": "Миссии",
            },
        ),
        migrations.CreateModel(
            name="Restaurant",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=150, verbose_name="Название")),
                ("city", models.CharField(max_length=150, verbose_name="Город")),
                (
                    "tables_count",
                    models.SmallIntegerField(
                        default=10, verbose_name="Количество столов"
                    ),
                ),
                (
                    "scheme_tables",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=restaurant.models.upload_for_restaurant,
                        verbose_name="Фото",
                    ),
                ),
            ],
            options={
                "verbose_name": "Ресторан",
                "verbose_name_plural": "Рестораны",
            },
        ),
        migrations.CreateModel(
            name="Services",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "service",
                    models.CharField(max_length=100, verbose_name="Услуга ресторана"),
                ),
                (
                    "is_published",
                    models.BooleanField(
                        default=True, verbose_name="Признак публикации"
                    ),
                ),
            ],
            options={
                "verbose_name": "Услуга",
                "verbose_name_plural": "Услуги",
            },
        ),
        migrations.CreateModel(
            name="StaffRestaurant",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("first_name", models.CharField(max_length=75, verbose_name="Имя")),
                ("last_name", models.CharField(max_length=75, verbose_name="Фамилия")),
                (
                    "photo",
                    models.ImageField(
                        blank=True,
                        default="non_avatar.png",
                        null=True,
                        upload_to=restaurant.models.upload,
                        verbose_name="Фото",
                    ),
                ),
                ("position", models.CharField(max_length=50, verbose_name="Должность")),
                (
                    "date_employment",
                    models.DateField(
                        blank=True, null=True, verbose_name="Дата трудоустройства"
                    ),
                ),
                (
                    "is_published",
                    models.BooleanField(default=True, verbose_name="Публикация"),
                ),
            ],
            options={
                "verbose_name": "Персонал",
                "verbose_name_plural": "Персонал",
            },
        ),
    ]
