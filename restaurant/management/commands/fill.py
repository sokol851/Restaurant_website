from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        """
        Создаём контент! Включая админа, если не создан.
        """
        from django.core.management import call_command

        if not User.objects.filter(email="admin@pow.ru"):
            call_command("csu")
        call_command("loaddata", "fixtures/restaurant.json")
        print("Создан контент сайта")
