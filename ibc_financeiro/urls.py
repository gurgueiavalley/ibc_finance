from django.urls import path
from . import views

urlpatterns = [
    path('relatorio', views.relatorio, name='relatorio'),
    path('cadMembrosExcel', views.cadMembrosExcel, name='cadMembrosExcel'),
    path('', views.index, name = 'index'),
]