from django.forms import BooleanField
from django import forms


class StyleFormMixin:
    """Миксин для изменения аттрибутов стилей."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
            if isinstance(field, BooleanField):
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = "form-control"


class ContactForm(forms.Form):
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=20, required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
