from django import forms


def check_amount(value):
    if value < 500:
        raise forms.ValidationError("Сумма должна быть выше 500 руб.")
    else:
        return value
