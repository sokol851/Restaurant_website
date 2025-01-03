from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView

from config import settings
from restaurant.forms import ContactForm
from restaurant.models import (Description, HistoryRestaurant,
                               MissionsRestaurant, Restaurant, Services,
                               StaffRestaurant)
from restaurant.tasks import task_send_mail


class Index(TemplateView, FormView):
    """
    Контроллер главной страницы сайта
    """

    template_name = "restaurant/index.html"
    form_class = ContactForm
    success_url = reverse_lazy("restaurant:index")

    def form_valid(self, form):
        # Получаем данные из формы
        email = form.cleaned_data["email"]
        phone = form.cleaned_data["phone"]
        message = form.cleaned_data["message"]

        # Формируем письмо
        subject = 'Обратная связь для "Ресторан домашней кухни"'
        body = f"Email: {email}\n" \
               f"Телефон: {phone}\n"\
               f"Сообщение:\n{message}"
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [settings.EMAIL_HOST_USER, email]

        # Отправляем задачу отправки письма
        task_send_mail.delay(subject, body, from_email, recipient_list)

        # Появляется отображение успешной отправки
        messages.success(self.request, "Ваше сообщение отправлено!")

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["description"] = Description.objects.filter(is_published=True)
        context["services"] = Services.objects.filter(is_published=True)
        context["restaurant"] = Restaurant.objects.filter(is_published=True)
        return context


class AboutView(TemplateView):
    """
    Контроллер для страницы о ресторане.
    """

    template_name = "restaurant/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["history"] = HistoryRestaurant.objects.order_by("-year")
        context["missions"] = (MissionsRestaurant.objects.
                               order_by("serial_number"))
        context["staff"] = StaffRestaurant.objects.filter(is_published=True)
        context["title"] = "О ресторане"
        return context
