from django.shortcuts import render
from django.views.generic import TemplateView

class IndexView(TemplateView):
    template_name = r'login/templates/index.html'
    redirect_field_name = 'redirect_to'
