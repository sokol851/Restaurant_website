# Generated by Django 5.1.3 on 2024-11-26 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("restaurant", "0008_remove_staffrestaurant_experience_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="staffrestaurant",
            name="date_employment",
            field=models.DateField(
                blank=True, null=True, verbose_name="Дата трудоустройства"
            ),
        ),
    ]
