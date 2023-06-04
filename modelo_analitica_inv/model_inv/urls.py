from django.urls import path

from .views import IndexView
from .views import AILoginView
from .views import AILogoutView

app_name = 'modelo'
urlpatterns = [
    path('', IndexView.as_view(), name='home'),

]