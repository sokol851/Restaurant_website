# Generated by Django 5.1.3 on 2024-12-01 14:55

import datetime
import reservations.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("reservations", "0019_alter_reservation_create_at_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="reservation",
            name="amount",
            field=models.IntegerField(
                default=500,
                validators=[reservations.validators.check_amount],
                verbose_name="Депозит",
            ),
        ),
        migrations.AlterField(
            model_name="reservation",
            name="create_at",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 12, 1, 17, 55, 4, 114360),
                verbose_name="Время создания",
            ),
        ),
    ]