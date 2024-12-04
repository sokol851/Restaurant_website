from django import forms
import re


def check_amount(value):
    """ Проверка суммы депозита в пределах 500-10000 руб. """
    if value < 500:
        raise forms.ValidationError(
            "Сумма депозита должна быть выше 500 руб.")
    if value > 10000:
        raise forms.ValidationError(
            "Сумма депозита слишком большая, возможно вы ошиблись.")
    else:
        return value


def phone_number(value):
    """ Проверка правильности номера телефона """
    if re.match(r'^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]'
                r'?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$', value):
        return value
    else:
        raise forms.ValidationError("Введите настоящий номер телефона в РФ")
