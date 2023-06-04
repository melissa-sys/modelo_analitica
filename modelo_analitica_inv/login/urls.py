from django.urls import path

from .views import LoginIndexView
from .views import AILoginView
from .views import AILogoutView

app_name = 'login'
urlpatterns = [
    path('login', LoginIndexView.as_view(), name='home'),
    path('', AILoginView.as_view(), name='index'),
    path('logout', AILogoutView.as_view(), name='goodbye')

]