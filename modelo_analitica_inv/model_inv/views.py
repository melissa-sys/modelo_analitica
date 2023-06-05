from django.shortcuts import render

from django.views.generic import View
from django.views.generic import TemplateView
from django.shortcuts import HttpResponse

class IndexView(TemplateView):
    template_name = r'model_inv/templates/index.html'
    redirect_field_name = 'redirect_to'

class ModelView(TemplateView): 
    template_name = r'model_inv/templates/client_info.html'
    redirect_field_name = 'redirect_to'

    def post(self, request):
        doc = request.POST.get('doc', None)
        context = { 'num_doc': doc}
        return render(request, self.template_name, context)