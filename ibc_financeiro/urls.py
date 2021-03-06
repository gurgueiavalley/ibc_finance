from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name = 'index'),
    path('relatorio/<tipo>', relatorio, name = 'relatorio'),                # Relatório
    path('saida/<acao>', saida, name = 'saida'),                            # Saída
    path('congregacao/<acao>', congregacao, name = 'congregacao'),          # Congregação
    path('categoria/<acao>', categoria, name = 'categoria'),                # Categoria de Saída
    path('pagamento/<acao>', pagamento, name = 'pagamento'),                # Pagamento
    path('empresa/<acao>', empresa, name = 'empresa'),                      # Empresa
    path('entrada/<acao>', entrada, name = 'entrada'),                      # Entrada
    path('catentrada/<acao>', catEntrada, name = 'catentrada'),             # Categoria de Entrada
    path('listar/<tipo>', listar, name = 'listar'),                         #Listar *
    path('membro/<acao>', membro, name = 'membro'),                         # Membro
    path('avulso/<acao>', avulso, name = 'avulso'),                         # Avulso
    path('emissao/<acao>', emissao, name = 'emissao'),                      # Entrada de Missão
    path('missao/<acao>', missao, name = 'missao'),                         # Missão
    path('conta/<acao>', conta, name = 'conta'),              # Autenticação User
    path('usuario/<acao>', usuario, name = 'usuario'),
]