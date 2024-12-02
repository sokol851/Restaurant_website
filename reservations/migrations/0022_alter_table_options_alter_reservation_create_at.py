# Generated by Django 5.1.3 on 2024-12-01 17:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("reservations", "0021_reservation_link_reservation_session_id_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="table",
            options={
                "ordering": ["restaurant", "number", "datetime"],
                "verbose_name": "Столик",
                "verbose_name_plural": "Столики",
            },
        ),
        migrations.AlterField(
            model_name="reservation",
            name="create_at",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 12, 1, 20, 38, 4, 252021),
                verbose_name="Время создания",
            ),
        ),
    ]