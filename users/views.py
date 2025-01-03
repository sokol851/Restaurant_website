import random
import string

from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import (CreateView, DeleteView, DetailView, FormView,
                                  TemplateView, UpdateView)

from config import settings
from reservations.models import HistoryReservations
from restaurant.tasks import task_send_mail
from users.forms import (CustomLoginForm, UserPasswordResetForm,
                         UserProfileForm, UserRegisterForm)
from users.models import User


class RegisterView(CreateView):
    """
    Контроллер создания пользователя

    Методы:
        send_verification_email - отправка письма для верификации
    """

    model = User
    form_class = UserRegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:email_confirmation_sent")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Регистрация на сайте"
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.instance
        self.send_verification_email(user)
        return response

    @staticmethod
    def send_verification_email(user):
        """Отправка письма для подтверждения регистрации"""

        # Собираем письмо
        verification_link = \
            f"{settings.SITE_URL}/users/verify/{user.token_verify}/"

        subject = "Подтвердите регистрацию!"
        message = (
            f"Благодарим за регистрацию на сайте ресторана.\n"
            f"Для активации учётной записи, пожалуйста перейдите по ссылке:\n"
            f"{verification_link}"
        )
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [user.email]

        # Отправляем задачу в celery
        task_send_mail.delay(
            subject,
            message,
            from_email,
            recipient_list,
            fail_silently=False,
        )


class VerifyEmailView(View):
    """
    Контроллер верификации почты
    """

    @staticmethod
    def get(request, token_verify, *args, **kwargs):
        try:
            user = User.objects.get(token_verify=token_verify)
            user.is_active = True
            user.save()
            email = user.email
            title = "Регистрация завершена!"
            message = f"Аккаунт {email} успешно активирован!"
        except User.DoesNotExist:
            title = "Ошибка!"
            message = (
                "Произошла ошибка."
                " Убедитесь, что переходите по ссылке из письма!"
            )

        return render(
            request, "users/reg_confirm.html",
            {"message": message, "title": title}
        )


class EmailConfirmationSentView(TemplateView):
    """Контроллёр уведомления отправки верификации"""

    template_name = "users/email_confirmation_sent.html"


class ProfileDetailView(LoginRequiredMixin, DetailView):
    """
    Контроллер профиля пользователя
    """

    model = User

    def get_object(self, queryset=None):
        self.user = super().get_object(queryset)
        if self.request.user == self.user or self.request.user.is_superuser:
            return self.user
        raise PermissionDenied

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["history_reservations"] = (HistoryReservations.objects.all().
                                           filter(user=self.request.user))
        return context


class ProfileDeleteView(LoginRequiredMixin, DeleteView):
    """
    Контроллер удаления профиля пользователя
    """

    model = User
    success_url = reverse_lazy("restaurant:index")

    def get_object(self, queryset=None):
        self.user = super().get_object(queryset)
        if self.request.user == self.user or self.request.user.is_superuser:
            return self.user
        raise PermissionDenied


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """
    Контроллер изменения профиля пользователя
    """

    model = User
    form_class = UserProfileForm

    def get_success_url(self):
        return reverse("users:user_detail", args=[self.kwargs.get("pk")])

    def form_valid(self, form):
        user = form.save()
        if user.phone is None:
            user.phone = "Не указано"
        if user.avatar == "":
            user.avatar = "non_avatar.png"
        user.save()
        return super().form_valid(form)

    def get_object(self, queryset=None):
        self.user = super().get_object(queryset)
        if self.request.user == self.user or self.request.user.is_superuser:
            return self.user
        raise PermissionDenied


class CustomLoginView(LoginView):
    """
    Контроллер формы авторизации
    """

    form_class = CustomLoginForm
    template_name = "users/login.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Авторизация"
        return context


class UserPasswordResetView(FormView):
    """
    Контроллёр сброса пароля
    """

    template_name = "users/user_password_reset.html"
    form_class = UserPasswordResetForm
    success_url = reverse_lazy("users:user_password_sent")

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        user = User.objects.filter(email=email).first()

        if user is not None:
            characters = string.ascii_letters + string.digits
            new_password = (
                "".join(random.choice(characters) for i in range(12)))

            user.password = make_password(new_password)
            user.save()

            subject = "Восстановление пароля"
            message = f"Ваш новый пароль: {new_password}"
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [email]

            task_send_mail.delay(subject, message, from_email, recipient_list)
        return super().form_valid(form)


class UserPasswordSentView(TemplateView):
    """
    Контроллёр успешной отправки нового пароля
    """

    template_name = "users/user_password_sent.html"
