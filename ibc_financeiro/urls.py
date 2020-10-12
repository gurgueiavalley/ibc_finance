from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('relatorioSaida', views.relatorioSaida, name = 'relatorioSaida'),
    
    path('cadMembrosExcel', views.cadMembrosExcel, name='cadMembrosExcel'),
    path('relatorio', views.relatorio, name='relatorio'),
]