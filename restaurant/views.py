from django.views.generic import TemplateView

from restaurant.models import HistoryRestaurant, MissionsRestaurant, StaffRestaurant


class Index(TemplateView):
    """
    Контроллер главной страницы сайта
    """

    template_name = "restaurant/index.html"


class AboutView(TemplateView):
    """
    Контроллер для страницы о ресторане.
    """

    template_name = 'restaurant/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['history'] = HistoryRestaurant.objects.order_by('-year')
        context['missions'] = MissionsRestaurant.objects.order_by('serial_number')
        context['staff'] = StaffRestaurant.objects.filter(is_published=True)
        context['title'] = 'О ресторане'
        return context
