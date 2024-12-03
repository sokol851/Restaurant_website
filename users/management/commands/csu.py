from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        if not User.objects.filter(email='admin@pow.ru'):
            user = User.objects.create(
                email="admin@pow.ru",
                first_name="Admin",
                last_name="Adminov",
                is_staff=True,
                is_superuser=True,
                is_active=True,
            )

            user.set_password("12345")
            user.save()
            print('Создан администратор "admin@pow.ru"')
        else:
            print('Админ уже существует!')
