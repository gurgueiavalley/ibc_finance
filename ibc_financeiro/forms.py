from django import forms
from .models import *

class FormExcel(forms.Form):
    arquivo = forms.FileField()
    arquivo.widget.attrs["class"] = "form-control"

class SaidaRelatorioForm(forms.Form):
    categoria = forms.ModelMultipleChoiceField(to_field_name = 'nome', label = 'Categoria(s)', queryset = CategoriaSaida.objects.all().order_by('nome'), required = False)
    categoria.widget.attrs['title'] = 'Nenhuma selecionada'
    categoria.widget.attrs['class'] = 'form-control'

    empresa = forms.ModelMultipleChoiceField(to_field_name = 'nome', label = 'Empresa(s)', queryset = Empresa.objects.all().order_by('nome'), required = False)
    empresa.widget.attrs['title'] = 'Nenhuma selecionada'    
    empresa.widget.attrs['class'] = 'form-control'



# inicio = forms.DateField(label = 'Data de Início')
# fim = forms.DateField(label = 'Data de Fim')
# pagamento = forms.ModelChoiceField(required = False, queryset = Pagamento.objects.all(), empty_label = 'Escolha a forma de pagamento')