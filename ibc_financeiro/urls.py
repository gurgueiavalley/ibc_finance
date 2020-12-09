from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name = 'index'),
    path('cadMembrosExcel', cadMembrosExcel, name='cadMembrosExcel'),
    path('relatorio/<tipo>', relatorio, name = 'relatorio'),                # Relatório
    path('saida/<acao>', saida, name = 'saida'),                            # Saída
    path('congregacao/<acao>', congregacao, name = 'congregacao'),          # Congregação
    path('categoria/<acao>', categoria, name = 'categoria'),                # Categoria
    path('pagamento/<acao>', pagamento, name = 'pagamento'),                # Pagamento
    path('empresa/<acao>', empresa, name = 'empresa'),                  # Empresa
]