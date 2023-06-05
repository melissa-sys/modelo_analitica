from django.views.generic import TemplateView


class LoginIndexView(TemplateView):
    template_name = r'login/templates/index.html'
    redirect_field_name = 'redirect_to'


