from django.shortcuts import render
from django.views.generic import TemplateView

class IndexView(TemplateView):
    template_name = r'model_inv/templates/client_info.html'
    redirect_field_name = 'redirect_to'
