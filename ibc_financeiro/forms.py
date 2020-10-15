from django import forms
from .models import CategoriaSaida

class FormExcel(forms.Form):
    arquivo = forms.FileField()
    arquivo.widget.attrs["class"] = "form-control"

class SaidaRelatorioForm(forms.Form):
    categoria = forms.ModelMultipleChoiceField(required = False,queryset = CategoriaSaida.objects.all())



# inicio = forms.DateField(label = 'Data de Início')
# fim = forms.DateField(label = 'Data de Fim')
# empresa = forms.ModelChoiceField(required = False, queryset = Empresa.objects.all(), empty_label = 'Escolha uma empresa')
# pagamento = forms.ModelChoiceField(required = False, queryset = Pagamento.objects.all(), empty_label = 'Escolha a forma de pagamento')