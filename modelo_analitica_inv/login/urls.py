from django.urls import path

from .views import LoginIndexView

app_name = 'login'
urlpatterns = [
    path('', LoginIndexView.as_view(), name='home')

]