from django import forms
from django.core.exceptions import ValidationError

from reservations.models import Reservation, Table
from restaurant.forms import StyleFormMixin
from restaurant.models import Restaurant


class ReservationUpdateForm(StyleFormMixin, forms.ModelForm):
    """Форма для обновления резервирований"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Уменьшаем размер поля комментария
        self.fields["comment"] = forms.CharField(
            required=False,
            widget=forms.Textarea(
                attrs={"rows": "3", "class": "form-control"}))
        self.fields["comment"].label = "Ваше сообщение"

    # Список уникальных номеров столов
    unique_numbers_values = sorted(set(Table.objects.
                                       values_list('number', flat=True)))

    table_number = forms.ChoiceField(
        choices=[(value, value) for value in unique_numbers_values],
        label="Номер стола",
        initial=None
    )

    # Список ресторанов
    table_restaurant = forms.ModelChoiceField(
        queryset=Restaurant.objects.all(), label="Ресторан", empty_label=None)

    # Список уникального времени столов
    unique_is_datetime_values = sorted(set(
        Table.objects.values_list('is_datetime', flat=True).
        filter(available=True)))

    table_is_datetime = forms.ChoiceField(
        choices=[(value, value) for value in unique_is_datetime_values],
        label="Дата и время",
        initial=None
    )

    def save(self, commit=True):
        # Получаем введённые данные
        reservation = super().save(commit=False)
        table_number = self.cleaned_data.get("table_number")
        table_restaurant = self.cleaned_data.get("table_restaurant")
        table_is_datetime = self.cleaned_data.get("table_is_datetime")

        # Пытаемся получить собранный стол из данных
        table = Table.objects.get(
            number=table_number,
            restaurant=table_restaurant,
            is_datetime=table_is_datetime,
            available=True
        )

        # Полученный стол присваиваем полю table
        reservation.table = table
        if commit:
            reservation.save()
        return reservation

    def clean(self):
        # Собираем данные из формы
        cleaned_data = super().clean()
        table_number = self.cleaned_data.get("table_number")
        table_restaurant = self.cleaned_data.get("table_restaurant")
        table_is_datetime = self.cleaned_data.get("table_is_datetime")

        try:
            # Проверка на существование стола
            Table.objects.get(
                number=table_number,
                restaurant=table_restaurant,
                is_datetime=table_is_datetime,
                available=True
            )
        except Table.DoesNotExist:
            # Если нет - выдаём ошибку
            raise ValidationError(
                "Столик на выбранное время уже забронирован "
                "или не существует выбранном ресторане.")
        return cleaned_data

    class Meta:
        model = Reservation
        # fields = '__all__'
        exclude = (
            "user",
            "old_table",
            "create_at",
            "is_confirmed",
            "amount",
            "session_id",
            "link",
            "table",
        )


class ReservationCreateForm(StyleFormMixin, forms.ModelForm):
    """Форма для создания резервирований"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Уменьшаем размер поля комментария
        self.fields["comment"] = forms.CharField(
            required=False,
            widget=forms.Textarea(
                attrs={"rows": "3", "class": "form-control"}))
        self.fields["comment"].label = "Ваше сообщение"

    # Список уникальных номеров столов
    unique_numbers_values = sorted(set(Table.objects.
                                       values_list('number', flat=True)))

    table_number = forms.ChoiceField(
        choices=[(value, value) for value in unique_numbers_values],
        label="Номер стола",
        initial=None
    )

    # Список ресторанов
    table_restaurant = forms.ModelChoiceField(
        queryset=Restaurant.objects.all(), label="Ресторан", empty_label=None)

    # Список уникального времени столов
    unique_is_datetime_values = sorted(set(
        Table.objects.values_list('is_datetime', flat=True).
        filter(available=True)))

    table_is_datetime = forms.ChoiceField(
        choices=[(value, value) for value in unique_is_datetime_values],
        label="Дата и время",
        initial=None
    )

    def save(self, commit=True):
        # Получаем введённые данные
        reservation = super().save(commit=False)
        table_number = self.cleaned_data.get("table_number")
        table_restaurant = self.cleaned_data.get("table_restaurant")
        table_is_datetime = self.cleaned_data.get("table_is_datetime")

        # Пытаемся получить собранный стол из данных
        table = Table.objects.get(
            number=table_number,
            restaurant=table_restaurant,
            is_datetime=table_is_datetime,
            available=True
        )

        # Полученный стол присваиваем полю table
        reservation.table = table
        if commit:
            reservation.save()
        return reservation

    def clean(self):
        # Собираем данные из формы
        cleaned_data = super().clean()
        table_number = self.cleaned_data.get("table_number")
        table_restaurant = self.cleaned_data.get("table_restaurant")
        table_is_datetime = self.cleaned_data.get("table_is_datetime")

        try:
            # Проверка на существование стола
            Table.objects.get(
                number=table_number,
                restaurant=table_restaurant,
                is_datetime=table_is_datetime,
                available=True
            )
        except Table.DoesNotExist:
            # Если нет - выдаём ошибку
            raise ValidationError(
                "Столик на выбранное время уже забронирован "
                "или не существует выбранном ресторане.")
        return cleaned_data

    class Meta:
        model = Reservation
        # fields = '__all__'
        exclude = (
            "user",
            "old_table",
            "create_at",
            "is_confirmed",
            "session_id",
            "link",
            "table",
        )
