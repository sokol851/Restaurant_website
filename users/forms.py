from django import forms
from django.contrib.auth.forms import (AuthenticationForm, PasswordResetForm,
                                       UserChangeForm, UserCreationForm)

from restaurant.forms import StyleFormMixin
from users.models import User


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = (
            "email",
            "password1",
            "password2",
            "avatar",
        )


class UserProfileForm(StyleFormMixin, UserChangeForm):
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
                "Имя не может быть пустым или иметь цифры"
            )
        else:
            for word in self.list_stop_word:
                if word.lower() in clean_data.lower():
                    raise forms.ValidationError(
                        "Имя не может быть пустым или иметь цифры"
                    )
        return clean_data


class CustomLoginForm(StyleFormMixin, AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(
        attrs={"autofocus": True})
    )


class UserPasswordResetForm(StyleFormMixin, PasswordResetForm):
    class Meta:
        model = User
        fields = ("email",)
