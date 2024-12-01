# Generated by Django 5.1.3 on 2024-12-01 16:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("reservations", "0020_alter_reservation_amount_alter_reservation_create_at"),
    ]

    operations = [
        migrations.AddField(
            model_name="reservation",
            name="link",
            field=models.URLField(
                blank=True, max_length=500, null=True, verbose_name="Cсылка на оплату"
            ),
        ),
        migrations.AddField(
            model_name="reservation",
            name="session_id",
            field=models.CharField(
                blank=True, max_length=150, null=True, verbose_name="Сессия"
            ),
        ),
        migrations.AlterField(
            model_name="reservation",
            name="create_at",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 12, 1, 19, 49, 39, 401794),
                verbose_name="Время создания",
            ),
        ),
    ]
