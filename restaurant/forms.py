from django import forms


class StyleFormMixin:
    """Миксин для изменения аттрибутов стилей."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"


class ContactForm(forms.Form):
    """Форма для отправки обратной связи"""

    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=20, required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
