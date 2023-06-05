from django.shortcuts import render

from django.views.generic import View
from django.views.generic import TemplateView
from django.shortcuts import HttpResponse

from . import functions as f

class IndexView(TemplateView):
    template_name = r'model_inv/templates/index.html'
    redirect_field_name = 'redirect_to'
    

class ModelView(TemplateView): 
    template_name = r'model_inv/templates/client_info.html'
    redirect_field_name = 'redirect_to'

    def post(self, request):
        f.cargue_bd()
        doc = request.POST.get('doc', None)
        info_cliente = f.consulta_bd(doc)
        print(type(info_cliente[0]['cluster']))
        clasificacion = f.consulta_tipo_cliente(str(info_cliente[0]['cluster']))
        print(clasificacion)
        context = { 'info': info_cliente, 
                    'cluster': clasificacion}
        return render(request, self.template_name, context)

# Cargue BD

def load_dataset(request):
    f.cargue_bd(request)
    return HttpResponse('Cargue OK')