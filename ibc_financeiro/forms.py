from django import forms
from .models import CategoriaSaida

class FormExcel(forms.Form):
    arquivo = forms.FileField()
    arquivo.widget.attrs["class"] = "form-control"

class SaidaRelatorioForm(forms.Form):
    categoria = forms.ModelMultipleChoiceField(to_field_name = 'nome', label = 'Categoria(s)', queryset = CategoriaSaida.objects.all(), required = False)

    categoria.widget.attrs['title'] = 'Nenhuma selecionada'
    categoria.widget.attrs['class'] = 'form-control'



# inicio = forms.DateField(label = 'Data de Início')
# fim = forms.DateField(label = 'Data de Fim')
# empresa = forms.ModelChoiceField(required = False, queryset = Empresa.objects.all(), empty_label = 'Escolha uma empresa')
# pagamento = forms.ModelChoiceField(required = False, queryset = Pagamento.objects.all(), empty_label = 'Escolha a forma de pagamento')