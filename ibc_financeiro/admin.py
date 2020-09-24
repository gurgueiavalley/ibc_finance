from django.contrib import admin
from ibc_financeiro.models import *
from django.contrib.auth.models import Group, User

admin.site.register(AdminCongregacao)
admin.site.register(Contador)
admin.site.register(Empresa)
admin.site.register(EntradaMissao)
admin.site.register(Missao)
admin.site.register(Saida)
admin.site.register(SaidaCategoria)

admin.site.site_header="IBC FINANCEIRO"
admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(Membro)
admin.site.register(CategoriaEntrada)
admin.site.register(FormaPagamento)
admin.site.register(Congregacao)
admin.site.register(EntradaFinanceiraAvulca)
admin.site.register(EntradaFinanceira)