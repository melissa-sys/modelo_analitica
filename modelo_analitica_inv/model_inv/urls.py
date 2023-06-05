from django.urls import path

from . import views
from .views import IndexView
from .views import ModelView


app_name = 'modelo'
urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('info_cliente', ModelView.as_view(), name='informacion'),

    # Cargue BD
    path('dataset_load', views.load_dataset, name='cargue_bd'),
]