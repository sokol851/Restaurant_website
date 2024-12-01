# Generated by Django 5.1.3 on 2024-11-28 19:02

import restaurant.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("restaurant", "0016_alter_contacts_extra_alter_contacts_phone"),
    ]

    operations = [
        migrations.AddField(
            model_name="description",
            name="background",
            field=models.ImageField(
                blank=True,
                default="non_avatar.png",
                null=True,
                upload_to=restaurant.models.upload_for_bg,
                verbose_name="Фон",
            ),
        ),
    ]
