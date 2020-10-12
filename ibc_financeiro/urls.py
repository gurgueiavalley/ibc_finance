from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('cadMembrosExcel', views.cadMembrosExcel, name='cadMembrosExcel'),
    path('relatorio', views.relatorio, name='relatorio'),
]