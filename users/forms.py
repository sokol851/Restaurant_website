import re

from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordResetForm,
    UserChangeForm,
    UserCreationForm,
)

from restaurant.forms import StyleFormMixin
from users.models import User


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    """Форма регистрации пользователя"""

    class Meta:
        model = User
        fields = (
            "email",
            "password1",
            "password2",
            "avatar",
        )


class UserProfileForm(StyleFormMixin, UserChangeForm):
    """Форма изменения пользователя"""

    list_stop_word = \
        ["Не указано", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]

    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "phone",
            "avatar",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password"].widget = forms.HiddenInput()

    def clean_first_name(self):
        """Фильтрация запрещённых слов в названии"""
        clean_data = self.cleaned_data["first_name"]

        if clean_data is None:
            raise forms.ValidationError(
                "Имя не может быть пустым или иметь цифры")
        else:
            for word in self.list_stop_word:
                if word.lower() in clean_data.lower():
                    raise forms.ValidationError(
                        "Имя не может быть пустым или иметь цифры"
                    )
        return clean_data

    def clean_last_name(self):
        """Фильтрация запрещённых слов в названии"""
        clean_data = self.cleaned_data["last_name"]

        if clean_data is None:
            raise forms.ValidationError(
                "Фамилия не может быть пустой или иметь цифры")
        else:
            for word in self.list_stop_word:
                if word.lower() in clean_data.lower():
                    raise forms.ValidationError(
                        "Фамилия не может быть пустой или иметь цифры"
                    )
        return clean_data

    def clean_phone(self):
        """Валидация правильности номера телефона"""
        clean_data = self.cleaned_data["phone"]
        if clean_data is None:
            clean_data = "Не указано"
        if clean_data != "Не указано":
            if re.match(
                r"^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]"
                r"?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$",
                clean_data,
            ):
                return clean_data
            else:
                raise forms.ValidationError(
                    "Введите настоящий номер телефона в РФ")
        return clean_data


class CustomLoginForm(StyleFormMixin, AuthenticationForm):
    """Форма аутентификации по email"""

    username = forms.EmailField(widget=forms.EmailInput(
        attrs={"autofocus": True}))


class UserPasswordResetForm(StyleFormMixin, PasswordResetForm):
    """Форма сброса пароля"""

    class Meta:
        model = User
        fields = ("email",)
