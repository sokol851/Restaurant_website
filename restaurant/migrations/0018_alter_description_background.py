# Generated by Django 5.1.3 on 2024-11-28 19:03

import restaurant.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("restaurant", "0017_description_background"),
    ]

    operations = [
        migrations.AlterField(
            model_name="description",
            name="background",
            field=models.ImageField(
                upload_to=restaurant.models.upload_for_bg, verbose_name="Фон"
            ),
        ),
    ]
