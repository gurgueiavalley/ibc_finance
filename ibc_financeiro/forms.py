from django import forms
from .models import *

class FormExcel(forms.Form):
    arquivo = forms.FileField()
    arquivo.widget.attrs["class"] = "form-control"

class SaidaRelatorioForm(forms.Form):
    inicio = forms.DateField(label = 'De')
    inicio.widget.attrs = {'class' : 'form-control', 'placeholder' : 'Selecione a data'}

    fim = forms.DateField(label = 'Até')
    
    congregacao = forms.ModelMultipleChoiceField(label = 'Congregação(ões)', required = False, queryset = Congregacao.objects.all().order_by('nome'), to_field_name = 'nome')

    categoria = forms.ModelMultipleChoiceField(label = 'Categoria(s)', required = False, queryset = CategoriaSaida.objects.all().order_by('nome'), to_field_name = 'nome')
    categoria.widget.attrs = {'class' : 'form-control', 'title' : 'Nenhuma selecionada'}

    pagamento = forms.ModelMultipleChoiceField(label = 'Forma(s) de Pagamento', required = False, queryset = Pagamento.objects.all().order_by('nome'), to_field_name = 'nome')
    pagamento.widget.attrs = {'class' : 'form-control', 'title' : 'Nenhuma selecionada'}

    empresa = forms.ModelMultipleChoiceField(label = 'Empresa(s)', required = False, queryset = Empresa.objects.all().order_by('nome'), to_field_name = 'nome')
    empresa.widget.attrs = {'class' : 'form-control', 'title' : 'Nenhuma selecionada'}

    minimo = forms.DecimalField(label = 'De', required = False, max_digits = 12, decimal_places = 2, min_value = Saida.objects.all().order_by('valor')[0].valor)
    maximo = forms.DecimalField(label = 'Até', required = False, max_digits = 12, decimal_places = 2, max_value = Saida.objects.all().order_by('-valor')[0].valor)