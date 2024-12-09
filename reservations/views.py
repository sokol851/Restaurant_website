from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from config.settings import CACHE_ENABLED
from reservations.forms import ReservationCreateForm, ReservationUpdateForm
from reservations.models import Reservation
from restaurant.models import Restaurant


class ReservationListView(LoginRequiredMixin, ListView):
    """
    Контроллер отображения списка броней.
    """

    model = Reservation

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        # Пользователь получает доступ только к своим записям
        # superuser получает доступ ко всем записям
        if not self.request.user.is_superuser:
            queryset = queryset.filter(user=self.request.user.pk)
        return queryset


class ReservationUpdateView(LoginRequiredMixin, UpdateView):
    """
    Контроллер редактирования броней.
    """

    model = Reservation
    form_class = ReservationUpdateForm
    success_url = reverse_lazy("reservations:list_reservations")

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        # Пользователь получает доступ только к своим записям
        # superuser получает доступ ко всем записям
        if (self.request.user == self.object.user or
                self.request.user.is_superuser):
            return self.object
        raise PermissionDenied

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Получаем объекты ресторанов для отображения схем.
        # Проверяем включенность кеша
        if CACHE_ENABLED:
            # Создаём ключ для хранения
            key = 'scheme_tables'
            # Пытаемся получить данные
            context["scheme_tables"] = cache.get(key)
            if context["scheme_tables"] is None:
                # Если данные не были получены из кеша,
                # то выбираем из БД и записываем в кеш
                context["scheme_tables"] = Restaurant.objects.all()
                cache.set(key, context["scheme_tables"])
        else:
            # Если кеш не был подключен, то просто обращаемся к БД
            context["scheme_tables"] = Restaurant.objects.all()
        return context


class ReservationCreateView(LoginRequiredMixin, CreateView):
    """
    Контроллер создания броней.
    """

    model = Reservation
    form_class = ReservationCreateForm
    success_url = reverse_lazy("reservations:list_reservations")

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Проверяем включенность кеша
        if CACHE_ENABLED:
            # Создаем ключ для хранения
            key = 'scheme_tables'
            # Пытаемся получить данные
            context["scheme_tables"] = cache.get(key)
            if context["scheme_tables"] is None:
                # Если данные не были получены из кеша,
                # то выбираем из БД и записываем в кеш
                context["scheme_tables"] = Restaurant.objects.all()
                cache.set(key, context["scheme_tables"])
        else:
            # Если кеш не был подключен, то просто обращаемся к БД
            context["scheme_tables"] = Restaurant.objects.all()
        return context


class ReservationDeleteView(LoginRequiredMixin,
                            DeleteView):
    model = Reservation
    success_url = reverse_lazy("reservations:list_reservations")

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        # Пользователь получает доступ только к своим записям
        # superuser получает доступ ко всем записям
        if (self.request.user == self.object.user or
                self.request.user.is_superuser):
            return self.object
        raise PermissionDenied
