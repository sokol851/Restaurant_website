from datetime import timedelta

from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from reservations.models import Reservation, Table
from restaurant.forms import StyleFormMixin


class ReservationUpdateForm(StyleFormMixin, forms.ModelForm):
    """Форма для обновления резервирований"""

    # Новые поля формы
    table_number = forms.ChoiceField(choices=None,
                                     label="Номер стола",
                                     initial=None)
    table_restaurant = forms.ModelChoiceField(queryset=None,
                                              label="Ресторан",
                                              empty_label=None)
    table_is_datetime = forms.ChoiceField(
        choices=None,
        label="Дата и время",
        initial=None
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Импорт моделей после инициализации, избегаем ошибки при миграциях.
        from reservations.models import Table
        from restaurant.models import Restaurant

        # Уменьшаем размер поля комментария
        self.fields["comment"] = forms.CharField(
            required=False,
            widget=forms.Textarea(
                attrs={"rows": "3", "class": "form-control"}))
        self.fields["comment"].label = "Ваше сообщение"

        # за 15 минут до события столик становится недоступен для брони.
        event_time = timezone.localtime(timezone.now()) + timedelta(minutes=15)

        # Получаем queryset модели столов
        tables = (Table.objects.all().filter(available=True).
                  filter(is_datetime__gt=event_time))

        # Присваиваем значения полям формы
        self.fields['table_number'].choices = \
            [(value, value) for value in
             sorted(set(tables.values_list('number', flat=True)))]
        self.fields['table_restaurant'].queryset = Restaurant.objects.all()
        self.fields['table_is_datetime'].choices = \
            [(value, value) for value in
             sorted(set(tables.values_list('is_datetime', flat=True).
                        filter(available=True)))]

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

    table_number = forms.ChoiceField(choices=None,
                                     label="Номер стола",
                                     initial=None)
    table_restaurant = forms.ModelChoiceField(queryset=None,
                                              label="Ресторан",
                                              empty_label=None)
    table_is_datetime = forms.ChoiceField(
        choices=None,
        label="Дата и время",
        initial=None
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Импорт моделей после инициализации, избегаем ошибки при миграциях.
        from reservations.models import Table
        from restaurant.models import Restaurant

        # Уменьшаем размер поля комментария
        self.fields["comment"] = forms.CharField(
            required=False,
            widget=forms.Textarea(
                attrs={"rows": "3", "class": "form-control"}))
        self.fields["comment"].label = "Ваше сообщение"

        # за 15 минут до события столик становится недоступен для брони.
        event_time = timezone.localtime(timezone.now()) + timedelta(minutes=15)

        # Получаем queryset модели столов
        tables = (Table.objects.all().filter(available=True).
                  filter(is_datetime__gt=event_time))

        # Присваиваем значения полям формы
        self.fields['table_number'].choices = \
            [(value, value) for value in
             sorted(set(tables.values_list('number', flat=True)))]
        self.fields['table_restaurant'].queryset = Restaurant.objects.all()
        self.fields['table_is_datetime'].choices = \
            [(value, value) for value in
             sorted(set(tables.values_list('is_datetime', flat=True).
                        filter(available=True)))]

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
