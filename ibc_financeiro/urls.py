from django.urls import path
from . import views

urlpatterns = [
    path('cadastroMembrosExcel/', views.cadMembrosExcel, name='cadMembrosExcel'),
    path('', views.index, name = 'index'),
]