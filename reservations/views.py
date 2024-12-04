from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

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
    success_url = reverse_lazy("restaurant:index")

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
        # Получаем объекты ресторанов для отображения схем.
        context["scheme_tables"] = Restaurant.objects.all()
        return context


class ReservationDeleteView(LoginRequiredMixin,
                            UserPassesTestMixin,
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

    def test_func(self):
        return self.request.user.is_superuser
