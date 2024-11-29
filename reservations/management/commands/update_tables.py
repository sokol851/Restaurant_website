from datetime import date

from django.core.management import BaseCommand

from reservations.models import Table


class Command(BaseCommand):

    def handle(self, *args, **options):
        numbers_table = Table.objects.all()

        for table in numbers_table:
            table = Table.objects.filter(id=table.id).update(
                date=date.today(), # Дата сегодня
                # date=date(2024, 11, 30), # Или можно установить нужную дату
                available = True,
            )
            print(table)
