from django import forms
from .models import *

class FormExcel(forms.Form):
    arquivo = forms.FileField()

class FiltrosRelatorioSaida(forms.Form):
    inicio = forms.DateField(label = 'Data de Início')
    fim = forms.DateField(label = 'Data de Fim')
    categoria = forms.ModelChoiceField(required = False, queryset = CategoriaSaida.objects.all(), empty_label = 'Escolha uma categoria')
    empresa = forms.ModelChoiceField(required = False, queryset = Empresa.objects.all(), empty_label = 'Escolha uma empresa')
    pagamento = forms.ModelChoiceField(required = False, queryset = Pagamento.objects.all(), empty_label = 'Escolha a forma de pagamento')