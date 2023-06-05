from django.urls import path

from .views import IndexView
from .views import ModelView


app_name = 'modelo'
urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('info_cliente', ModelView.as_view(), name='informacion'),

]