# Generated by Django 5.1.3 on 2024-11-26 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("restaurant", "0007_remove_missionsrestaurant_position_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="staffrestaurant",
            name="experience",
        ),
        migrations.AddField(
            model_name="staffrestaurant",
            name="date_employment",
            field=models.DateTimeField(
                blank=True, null=True, verbose_name="Дата трудоустройства"
            ),
        ),
    ]
