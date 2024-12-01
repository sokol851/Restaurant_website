from datetime import timedelta, datetime

from django.core.management import BaseCommand

from reservations.models import Table


class Command(BaseCommand):
    """
     Находит просроченные столы и
     обновляет дату и доступность на следующий день.
    """

    def handle(self, *args, **options):
        numbers_table = Table.objects.all()
        for table in numbers_table:
            if datetime.now().timestamp() > table.is_datetime.timestamp():
                Table.objects.filter(id=table.id).update(
                    is_datetime=table.is_datetime + timedelta(days=1),
                    available=True,
                )
