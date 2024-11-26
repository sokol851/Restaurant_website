# Generated by Django 5.1.3 on 2024-11-26 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
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
            ],
            options={
                "verbose_name": "Миссия",
                "verbose_name_plural": "Миссии",
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
                ("photo", models.ImageField(upload_to="staff", verbose_name="Фото")),
                ("position", models.CharField(max_length=50, verbose_name="Должность")),
                ("experience", models.CharField(max_length=50, verbose_name="Стаж")),
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
