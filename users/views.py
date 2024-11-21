from django.views.generic import CreateView

from users.models import User


class RegisterView(CreateView):
    model = User
