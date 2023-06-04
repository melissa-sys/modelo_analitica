from django.contrib import admin
from django.urls import path
from django.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('login.urls')),
    path('model', include('model_inv.urls'))
]
