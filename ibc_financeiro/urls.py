from django.urls    import path
from .views         import member

from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('membro/<action>', member, name = 'member'),

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
    path('avulso/<acao>', avulso, name = 'avulso'),                         # Avulso
    path('emissao/<acao>', emissao, name = 'emissao'),                      # Entrada de Missão
    path('missao/<acao>', missao, name = 'missao'),                         # Missão
    path('conta/<acao>', conta, name = 'conta'),              # Autenticação User
    path('usuario/<acao>', usuario, name = 'usuario'),

    path('password-reset', auth_views.PasswordResetView.as_view(template_name = 'financeiro/paginas/conta/password_reset.html', html_email_template_name = 'financeiro/paginas/conta/password_reset_email.html'), name= 'password_reset'),          # Formulário para informar o e-mail
    path('password-reset/done', auth_views.PasswordResetDoneView.as_view(template_name = 'financeiro/paginas/conta/password_reset_done.html'), name= 'password_reset_done'),                                                                        # Notificação de e-mail enviado
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name = 'financeiro/paginas/conta/password_reset_confirm.html'), name = 'password_reset_confirm'),                                         # Formulário para alterar a senha
    path('password-reset-complete', auth_views.PasswordResetCompleteView.as_view(template_name= 'financeiro/paginas/conta/password_reset_complete.html'), name= 'password_reset_complete'),                                                         # Confirmação de senha alterada
]