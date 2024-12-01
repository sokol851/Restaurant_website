# Generated by Django 5.1.3 on 2024-12-01 17:44

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("reservations", "0022_alter_table_options_alter_reservation_create_at"),
        ("restaurant", "0020_restaurant"),
    ]

    operations = [
        migrations.AlterField(
            model_name="reservation",
            name="create_at",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 12, 1, 20, 44, 14, 896536),
                verbose_name="Время создания",
            ),
        ),
        migrations.AlterField(
            model_name="table",
            name="restaurant",
            field=models.ForeignKey(
                choices=[],
                on_delete=django.db.models.deletion.CASCADE,
                to="restaurant.restaurant",
                verbose_name="Ресторан",
            ),
        ),
    ]
