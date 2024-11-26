# Generated by Django 5.1.3 on 2024-11-26 13:47

import users.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_alter_user_avatar"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="avatar",
            field=models.ImageField(
                blank=True,
                default="users/non_avatar.png",
                null=True,
                upload_to=users.models.upload_for_users,
                verbose_name="Аватар",
            ),
        ),
    ]
