# Generated by Django 5.1.3 on 2024-11-29 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("reservations", "0008_table_places"),
    ]

    operations = [
        migrations.AlterField(
            model_name="table",
            name="places",
            field=models.CharField(
                blank=True, max_length=30, null=True, verbose_name="Вместимость"
            ),
        ),
    ]
