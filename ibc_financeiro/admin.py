from django.contrib import admin
from django.contrib.auth.models import Group, User
from ibc_financeiro.models import *

class AdministradorAdmin(admin.ModelAdmin):
    actions = None
    list_display = 'username', 'nome', 'email',
    ordering = 'nome',
    search_fields = 'username', 'nome', 'email',

    fields = ('username', 'nome'), ('email', 'senha')

class CategoriasAdmin(admin.ModelAdmin):
    actions = None
    list_display = 'nome', 'descricao',
    ordering = 'nome',
    search_fields = 'nome',

admin.site.site_header = 'IBC Financeiro'

admin.site.unregister(Group)
admin.site.unregister(User)

admin.site.register(Administrador, AdministradorAdmin)
admin.site.register(CategoriaEntrada, CategoriasAdmin)
admin.site.register(CategoriaSaida, CategoriasAdmin)