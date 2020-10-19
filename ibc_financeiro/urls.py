from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name = 'index'),
    path('cadMembrosExcel', cadMembrosExcel, name='cadMembrosExcel'),
    path('relatorio', relatorio, name='relatorio'),
    path('relatorioSaida', relatorioSaida, name = 'relatorioSaida'),
]