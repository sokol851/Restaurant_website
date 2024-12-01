# Generated by Django 5.1.3 on 2024-11-28 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("restaurant", "0012_services"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="description",
            name="is_current",
        ),
        migrations.AddField(
            model_name="description",
            name="is_published",
            field=models.BooleanField(default=False, verbose_name="Признак публикации"),
        ),
        migrations.AddField(
            model_name="services",
            name="is_published",
            field=models.BooleanField(default=False, verbose_name="Признак публикации"),
        ),
    ]
