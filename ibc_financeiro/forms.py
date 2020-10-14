from django import forms
from . import models

class FormExcel(forms.Form):
    arquivo = forms.FileField()

class SaidaForm(forms.Form):
    categorias = []

    for category in CategoriaSaida.objects.all():
        categorias.append(category.nome)

    categoria = forms.ChoiceField(choices = [categorias], required= False)