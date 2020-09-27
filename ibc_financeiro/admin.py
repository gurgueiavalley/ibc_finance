from django.contrib import admin
from django.contrib.auth.models import Group, User
from ibc_financeiro.models import *

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
admin.site.register(Congregacao, SimplesAdmin)
admin.site.register(Contador, UsuarioAdmin)