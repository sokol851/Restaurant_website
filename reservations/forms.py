from django import forms

from reservations import models
from reservations.models import Reservation
from restaurant.forms import StyleFormMixin


class ReservationUpdateForm(StyleFormMixin, forms.ModelForm):
    """ Форма для обновления резервирований """

    class Meta:
        model = Reservation
        # fields = '__all__'
        exclude = ('user', 'old_table', 'create_at', 'is_confirmed', 'amount', 'session_id', 'link',)


class ReservationCreateForm(StyleFormMixin, forms.ModelForm):
    """ Форма для создания резервирований """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['table'].queryset = models.Table.objects.all().filter(available=True)

    class Meta:
        model = Reservation
        # fields = '__all__'
        exclude = ('user', 'old_table', 'create_at', 'is_confirmed', 'session_id', 'link',)
