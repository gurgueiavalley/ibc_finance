from django.contrib import admin
from django.contrib.auth.models import Group, User
from ibc_financeiro.models import *
import requests

class CongregacaoAdmin(admin.ModelAdmin):
    actions = None
    list_display = 'nome', 'localidade',
    ordering = 'nome',
    search_fields = 'nome',

class EmpresaAdmin(admin.ModelAdmin):
    actions = None
    list_display = 'CNPJ', 'nome', 'descricao',
    list_display_links = 'CNPJ', 'nome',
    list_filter = 'cidade',
    ordering = 'nome',
    search_fields = 'CNPJ', 'nome',

    fields = 'CNPJ',

    def save_model(self, request, obj, form, change):
        CNPJ = obj.CNPJ.replace('.', '').replace('/', '').replace('-', '')
        webservice = requests.get('http://receitaws.com.br/v1/cnpj/{}'.format(CNPJ))
        dados = webservice.json()
        
        if dados['fantasia'] != '':
            obj.nome = dados['fantasia']

        else:
            obj.nome = dados['nome']

        obj.CNPJ = dados['cnpj']
        obj.descricao = dados['atividade_principal'][0]['text']
        obj.endereco = dados['logradouro']
        obj.cidade = dados['municipio']

        super(EmpresaAdmin, self).save_model(request, obj, form, change)

class EntradaAdmin(admin.ModelAdmin):
    pass

class EntradaAvulsaAdmin(admin.ModelAdmin):
    actions = None
    list_display = '__str__', 'descricao', 'congregacao', 'data', 'administrador'
    list_filter = 'data', 'congregacao__localidade', 'administrador__nome',
    search_fields = 'valor', 'descricao',

    fields = ('valor', 'descricao'), ('congregacao', 'data'), 'comprovante', 'administrador' 

class EntradaMissaoAdmin(admin.ModelAdmin):
    actions = None
    list_display = '__str__', 'missao', 'data'
    list_filter = 'data', 'missao__nome', 'missao__congregacao__localidade',
    search_fields = 'valor',

class MissaoAdmin(admin.ModelAdmin):
    pass

class SimplesAdmin(admin.ModelAdmin):
    actions = None
    list_display = 'nome', 'descricao',
    ordering = 'nome',
    search_fields = 'nome',

class UsuarioAdmin(admin.ModelAdmin):
    actions = None
    list_display = 'username', 'nome', 'email',
    ordering = 'nome',
    search_fields = 'username', 'nome', 'email',

    fields = ('username', 'nome'), ('email', 'senha')

admin.site.site_header = 'IBC Financeiro'

admin.site.unregister(Group)
admin.site.unregister(User)

admin.site.register(Administrador, UsuarioAdmin)
admin.site.register(CategoriaEntrada, SimplesAdmin)
admin.site.register(CategoriaSaida, SimplesAdmin)
admin.site.register(Congregacao, CongregacaoAdmin)
admin.site.register(Contador, UsuarioAdmin)
admin.site.register(Empresa, EmpresaAdmin)
admin.site.register(Entrada, EntradaAdmin)              # PERSONALIZAR
admin.site.register(EntradaAvulsa, EntradaAvulsaAdmin)
admin.site.register(EntradaMissao, EntradaMissaoAdmin)
admin.site.register(Missao, MissaoAdmin)                # PERSONALIZAR