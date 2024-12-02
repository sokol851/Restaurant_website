from django.core.management import BaseCommand
from users.models import User


class Command(BaseCommand):
    """
    Создаём контент!
    """

    def handle(self, *args, **options):
        from django.core.management import call_command
        if not User.objects.filter(email='admin@pow.ru'):
            call_command('csu')
            print('Создан администратор "admin@pow.ru"')
        call_command('loaddata', 'fixtures/restaurant.json')
        print('Создан контент сайта')
