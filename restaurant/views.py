from django.views.generic import TemplateView


class Index(TemplateView):
    """
    Контроллер главной страницы сайта
    """

    template_name = "restaurant/index.html"
