# Generated by Django 5.1.3 on 2024-11-28 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("restaurant", "0013_remove_description_is_current_and_more"),
    ]

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
                        max_length=100, verbose_name="Дополнительная информация"
                    ),
                ),
                (
                    "phone",
                    models.CharField(max_length=15, verbose_name="Номер телефона"),
                ),
            ],
            options={
                "verbose_name": "Контакт",
                "verbose_name_plural": "Контакты",
            },
        ),
    ]
