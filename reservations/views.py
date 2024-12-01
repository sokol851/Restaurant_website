from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, CreateView

from reservations.forms import ReservationCreateForm, ReservationUpdateForm
from reservations.models import Reservation


class ReservationListView(LoginRequiredMixin, ListView):
    """
        Контроллер отображения списка броней.
    """
    model = Reservation

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(user=self.request.user.pk)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ReservationUpdateView(LoginRequiredMixin, UpdateView):
    """
        Контроллер редактирования броней.
    """
    model = Reservation
    form_class = ReservationUpdateForm
    success_url = reverse_lazy('restaurant:index')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user == self.object.user or self.request.user.is_superuser:
            return self.object
        raise PermissionDenied


class ReservationCreateView(LoginRequiredMixin, CreateView):
    """
        Контроллер создания броней.
    """
    model = Reservation
    form_class = ReservationCreateForm
    success_url = reverse_lazy('reservations:list_reservations')

    def form_valid(self, form):
        self.object = form.save()
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)
