from django import forms
from .models import *

class FormExcel(forms.Form):
    arquivo = forms.FileField()
    arquivo.widget.attrs["class"] = "form-control"

class SaidaRelatorioForm(forms.Form):
    inicio = forms.DateField(label = 'De:')
    inicio.widget.attrs = {'class' : 'form-control', 'placeholder' : 'Selecione a data'}

    fim = forms.DateField(label = 'Até:')
    fim.widget.attrs = {'class' : 'form-control', 'placeholder' : 'Selecione a data'}
    
    congregacao = forms.ModelMultipleChoiceField(label = 'Congregações', required = False, queryset = Congregacao.objects.all().order_by('nome'), to_field_name = 'nome')
    congregacao.widget.attrs = {'class' : 'form-control', 'title' : 'Nenhuma selecionada'}

    categoria = forms.ModelMultipleChoiceField(label = 'Categorias', required = False, queryset = CategoriaSaida.objects.all().order_by('nome'), to_field_name = 'nome')
    categoria.widget.attrs = {'class' : 'form-control', 'title' : 'Nenhuma selecionada'}

    pagamento = forms.ModelMultipleChoiceField(label = 'Formas de Pagamento', required = False, queryset = Pagamento.objects.all().order_by('nome'), to_field_name = 'nome')
    pagamento.widget.attrs = {'class' : 'form-control', 'title' : 'Nenhuma selecionada'}

    empresa = forms.ModelMultipleChoiceField(label = 'Empresas', required = False, queryset = Empresa.objects.all().order_by('nome'), to_field_name = 'nome')
    empresa.widget.attrs = {'class' : 'form-control', 'title' : 'Nenhuma selecionada'}

    minimo = forms.DecimalField(label = 'De:', required = False, max_digits = 12, decimal_places = 2, min_value = Saida.objects.all().order_by('valor')[0].valor)
    maximo = forms.DecimalField(label = 'Até:', required = False, max_digits = 12, decimal_places = 2, max_value = Saida.objects.all().order_by('-valor')[0].valor)