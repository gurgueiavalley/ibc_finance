from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('relatorio/<tipo>', views.relatorio, name = 'relatorio'),
    
    path('cadMembrosExcel', views.cadMembrosExcel, name='cadMembrosExcel'),
]