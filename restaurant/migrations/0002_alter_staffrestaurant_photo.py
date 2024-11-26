# Generated by Django 5.1.3 on 2024-11-26 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("restaurant", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="staffrestaurant",
            name="photo",
            field=models.ImageField(
                blank=True,
                default="users/non_avatar.png",
                null=True,
                upload_to="staff",
                verbose_name="Фото",
            ),
        ),
    ]
