from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('administracao/', admin.site.urls),
    path('', include('ibc_financeiro.urls')),
]