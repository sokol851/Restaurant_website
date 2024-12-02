# Generated by Django 5.1.3 on 2024-12-01 18:25

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("reservations", "0025_alter_reservation_create_at_alter_table_restaurant"),
        ("restaurant", "0020_restaurant"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="table",
            options={
                "ordering": ["restaurant", "number", "is_datetime"],
                "verbose_name": "Столик",
                "verbose_name_plural": "Столики",
            },
        ),
        migrations.RenameField(
            model_name="table",
            old_name="datetime",
            new_name="is_datetime",
        ),
        migrations.AlterField(
            model_name="reservation",
            name="create_at",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 12, 1, 21, 25, 36, 899370),
                verbose_name="Время создания",
            ),
        ),
        migrations.AlterField(
            model_name="table",
            name="restaurant",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="restaurant.restaurant",
                verbose_name="Ресторан",
            ),
        ),
    ]