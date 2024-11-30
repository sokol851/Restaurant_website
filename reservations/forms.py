from django import forms

from reservations.models import Reservation
from restaurant.forms import StyleFormMixin


class ReservationUpdateForm(StyleFormMixin, forms.ModelForm):
    """ Форма для резервирований """

    class Meta:
        model = Reservation
        # fields = '__all__'
        exclude = ('user', 'create_at', 'is_confirmed', 'amount')


class ReservationCreateForm(StyleFormMixin, forms.ModelForm):
    """ Форма для резервирований """

    class Meta:
        model = Reservation
        # fields = '__all__'
        exclude = ('user', 'create_at', 'is_confirmed',)
