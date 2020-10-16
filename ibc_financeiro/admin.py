from django.contrib import admin
from django.contrib.auth.models import Group, User
from ibc_financeiro.models import *

class CategoriaAdmin(admin.ModelAdmin):
    actions = None
    list_display = 'nome', 'descricao',
    ordering = 'nome',
    search_fields = 'nome',

class CongregacaoAdmin(admin.ModelAdmin):
    actions = None
    list_display = 'nome', 'localidade',
    ordering = 'nome',
    search_fields = 'nome',

class EmpresaAdmin(admin.ModelAdmin):
    actions = None
    list_display = 'CPF_CNPJ', 'nome', 'descricao',
    list_display_links = 'CPF_CNPJ', 'nome',
    list_filter = 'cidade',
    ordering = 'nome',
    search_fields = 'CPF_CNPJ', 'nome',

    fields = ('CPF_CNPJ', 'nome'), ('endereco', 'cidade'), 'descricao'    

class EntradaAdmin(admin.ModelAdmin):
    actions = None
    list_display = '__str__', 'categoria', 'membro', 'forma_de_Entrada', 'data'
    list_filter = 'categoria', 'data', 'forma_de_Entrada__nome', 'congregacao__nome', 'congregacao__localidade', 'administrador__nome'
    search_fields = 'membro__nome', 'valor'

    fields = ('categoria', 'valor', 'forma_de_Entrada'), 'descricao', ('membro', 'congregacao'), 'data', 'comprovante', 'administrador'

class EntradaAvulsaAdmin(admin.ModelAdmin):
    actions = None
    list_display = '__str__', 'descricao', 'congregacao', 'data'
    list_filter = 'data', 'congregacao__nome', 'congregacao__localidade', 'administrador__nome',
    search_fields = 'valor', 'descricao',

    fields = ('valor', 'descricao'), ('congregacao', 'data'), 'comprovante', 'administrador' 

class EntradaMissaoAdmin(admin.ModelAdmin):
    actions = None
    list_display = '__str__', 'missao', 'data'
    list_filter = 'data', 'missao__nome', 'missao__congregacao__nome',
    search_fields = 'valor',

class ExcelAdmin(admin.ModelAdmin):
    actions = None

class MembroAdmin(admin.ModelAdmin):
    actions = None
    list_display = 'CPF', 'nome', 'telefone', 'profissao'
    list_display_links = 'CPF', 'nome'
    ordering = 'nome',
    search_fields = 'CPF', 'nome', 'telefone', 'profissao'

    fields = ('CPF', 'nome'), ('telefone', 'profissao')

class MissaoAdmin(admin.ModelAdmin):
    actions = None
    list_display = 'nome', 'meta', 'em_Andamento', 'inicio', 'fim'
    list_filter = 'em_Andamento', 'inicio', 'fim', 'congregacao__nome', 'congregacao__localidade',
    search_fields = 'nome', 'meta'

    fields = ('nome', 'descricao'), ('congregacao', 'meta'), ('inicio', 'fim', 'em_Andamento')

class PagamentoAdmin(admin.ModelAdmin):
    actions = None
    list_display = 'nome',
    ordering = 'nome',
    search_fields = 'nome',

class SaidaAdmin(admin.ModelAdmin):
    actions = None
    list_display = 'nome', 'categoria', 'valor', 'forma_de_Pagamento', 'empresa', 'data'
    list_filter = 'data', 'categoria__nome', 'forma_de_Pagamento', 'empresa__nome', 'administrador__nome'
    search_fields = 'nome', 'valor'
    ordering = 'data',

    fields = 'categoria', ('nome', 'descricao'), 'data', ('valor', 'forma_de_Pagamento', 'empresa'), ('comprovante', 'nota_Fiscal'), 'administrador'

class UsuarioAdmin(admin.ModelAdmin):
    actions = None
    list_display = 'username', 'nome', 'email',
    ordering = 'nome',
    search_fields = 'username', 'nome', 'email',

    fields = ('username', 'nome'), ('email', 'senha')

admin.site.site_header = 'IBC Financeiro'

admin.site.unregister(Group)

admin.site.register(Administrador, UsuarioAdmin)
admin.site.register(CategoriaEntrada, CategoriaAdmin)
admin.site.register(CategoriaSaida, CategoriaAdmin)
admin.site.register(Congregacao, CongregacaoAdmin)
admin.site.register(Contador, UsuarioAdmin)
admin.site.register(Empresa, EmpresaAdmin)
admin.site.register(Entrada, EntradaAdmin)
admin.site.register(EntradaAvulsa, EntradaAvulsaAdmin)
admin.site.register(EntradaMissao, EntradaMissaoAdmin)
admin.site.register(Excel, ExcelAdmin)
admin.site.register(Membro, MembroAdmin)
admin.site.register(Missao, MissaoAdmin)
admin.site.register(Pagamento, PagamentoAdmin)
admin.site.register(Saida, SaidaAdmin)