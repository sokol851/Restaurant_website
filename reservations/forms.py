from datetime import timedelta

from django import forms
from django.utils import timezone

from reservations import models
from reservations.models import Reservation
from restaurant.forms import StyleFormMixin


class ReservationUpdateForm(StyleFormMixin, forms.ModelForm):
    """Форма для обновления резервирований"""

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
        )


class ReservationCreateForm(StyleFormMixin, forms.ModelForm):
    """Форма для создания резервирований"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Меняем размер поля комментария
        self.fields["comment"] = forms.CharField(
            widget=forms.Textarea(attrs={"rows": "3", "class": "form-control"})
        )
        self.fields["comment"].label = "Ваше сообщение"

        # за 15 минут до события столик становится недоступен для брони.
        event_time = timezone.localtime(timezone.now()) + timedelta(minutes=15)
        self.fields["table"].queryset = (
            models.Table.objects.all()
            .filter(available=True)
            .filter(is_datetime__gt=event_time)
        )

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
        )
