from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView

from reservations.forms import ReservationCreateForm, ReservationUpdateForm
from reservations.models import Reservation


class ReservationListView(ListView):
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


class ReservationUpdateView(UpdateView):
    """
        Контроллер редактирования броней.
    """
    model = Reservation
    form_class = ReservationUpdateForm
    success_url = reverse_lazy('restaurant:index')

    def post(self, request, pk):
        self.old_object = Reservation.objects.get(pk=pk)
        table = self.old_object.table
        table.available = True
        table.save()
        return super().post(request)

    def form_valid(self, form):
        self.object = form.save()
        table = self.object.table
        table.available = False
        table.save()
        return super().form_valid(form)

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user == self.object.user or self.request.user.is_superuser:
            return self.object
        raise PermissionDenied
