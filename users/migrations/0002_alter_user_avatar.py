# Generated by Django 5.1.3 on 2024-11-24 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="avatar",
            field=models.ImageField(
                blank=True,
                default="users/non_avatar.svg",
                null=True,
                upload_to="users/%Y",
                verbose_name="Аватар",
            ),
        ),
    ]