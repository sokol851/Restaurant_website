from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    UpdateView,
    CreateView,
    DeleteView
)

from reservations.forms import (
    ReservationCreateForm,
    ReservationUpdateForm
)
from reservations.models import Reservation
from reservations.services import (
    create_product,
    create_price,
    create_session
)


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
        if (self.request.user == self.object.user
                or self.request.user.is_superuser):
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

        # Создаём продукт
        stripe_product = create_product(product=self.object)
        # Создаём цену
        stripe_price = create_price(stripe_product, self.object.amount)
        # Создаём сессию и ссылку
        session_id, payment_link = create_session(stripe_price)

        # Присваиваем значения объекту
        self.object.user = self.request.user
        self.object.session_id = session_id
        self.object.link = payment_link
        self.object.save()
        return super().form_valid(form)


class ReservationDeleteView(LoginRequiredMixin,
                            UserPassesTestMixin,
                            DeleteView):
    model = Reservation
    success_url = reverse_lazy('reservations:list_reservations')

    def test_func(self):
        return self.request.user.is_superuser
