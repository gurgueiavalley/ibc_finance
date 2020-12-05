from django import forms
from .models import *

class FormExcel(forms.Form):
    arquivo = forms.FileField()
    arquivo.widget.attrs["class"] = "form-control"

class RelatorioEntradaForm(forms.Form):
    inicio = forms.DateField(label = 'De:')
    inicio.widget.attrs = {'class' : 'form-control', 'placeholder' : 'Selecione a data'}

    fim = forms.DateField(label = 'Até:')
    fim.widget.attrs = {'class' : 'form-control', 'placeholder' : 'Selecione a data'}

    congregacao = forms.ModelMultipleChoiceField(label = 'Congregações', required = False, queryset = Congregacao.objects.all().order_by('nome'), to_field_name = 'nome')
    congregacao.widget.attrs = {'class' : 'form-control', 'title' : 'Nenhuma selecionada'}

    categoria_entrada = forms.ModelMultipleChoiceField(label = 'Categorias', required = False, queryset = CategoriaEntrada.objects.all().order_by('nome'), to_field_name = 'nome')
    categoria_entrada.widget.attrs = {'class' : 'form-control', 'title' : 'Nenhuma selecionada'}

    forma = forms.ModelMultipleChoiceField(label = 'Formas de Entrada', required = False, queryset = Pagamento.objects.all().order_by('nome'), to_field_name = 'nome')
    forma.widget.attrs = {'class' : 'form-control', 'title' : 'Nenhuma selecionada'}

    membro = forms.ModelMultipleChoiceField(label = 'Membros', required = False, queryset = Membro.objects.all().order_by('nome'), to_field_name = 'nome')
    membro.widget.attrs = {'class' : 'form-control', 'title' : 'Nenhum selecionado'}

class RelatorioMissaoForm(forms.Form):
    inicio = forms.DateField(label = 'De:')
    inicio.widget.attrs = {'class' : 'form-control', 'placeholder' : 'Selecione a data'}

    fim = forms.DateField(label = 'Até:')
    fim.widget.attrs = {'class' : 'form-control', 'placeholder' : 'Selecione a data'}

    congregacao = forms.ModelMultipleChoiceField(label = 'Congregações', required = False, queryset = Congregacao.objects.all().order_by('nome'), to_field_name = 'nome')
    congregacao.widget.attrs = {'class' : 'form-control', 'title' : 'Nenhuma selecionada'}

    missao = forms.ModelMultipleChoiceField(label = 'Missões', required = False, queryset = Missao.objects.all().order_by('nome'), to_field_name = 'nome')
    missao.widget.attrs = {'class' : 'form-control', 'title' : 'Nenhuma selecionada'}

    andamento = forms.BooleanField(label = 'Em Andamento', required = False)

class RelatorioSaidaForm(forms.Form):
    inicio = forms.DateField(label = 'De:')
    inicio.widget.attrs = {'class' : 'form-control', 'placeholder' : 'Selecione a data'}

    fim = forms.DateField(label = 'Até:')
    fim.widget.attrs = {'class' : 'form-control', 'placeholder' : 'Selecione a data'}

    congregacao = forms.ModelMultipleChoiceField(label = 'Congregações', required = False, queryset = Congregacao.objects.all().order_by('nome'), to_field_name = 'nome')
    congregacao.widget.attrs = {'class' : 'form-control', 'title' : 'Nenhuma selecionada'}

    categoria_saida = forms.ModelMultipleChoiceField(label = 'Categorias', required = False, queryset = CategoriaSaida.objects.all().order_by('nome'), to_field_name = 'nome')
    categoria_saida.widget.attrs = {'class' : 'form-control', 'title' : 'Nenhuma selecionada'}

    pagamento = forms.ModelMultipleChoiceField(label = 'Formas de Pagamento', required = False, queryset = Pagamento.objects.all().order_by('nome'), to_field_name = 'nome')
    pagamento.widget.attrs = {'class' : 'form-control', 'title' : 'Nenhuma selecionada'}

    empresa = forms.ModelMultipleChoiceField(label = 'Empresas', required = False, queryset = Empresa.objects.all().order_by('nome'), to_field_name = 'nome')
    empresa.widget.attrs = {'class' : 'form-control', 'title' : 'Nenhuma selecionada'}

class RelatorioGeralForm(forms.Form):
    inicio = forms.DateField(label = 'De:')
    inicio.widget.attrs = {'class' : 'form-control', 'placeholder' : 'Selecione a data'}

    fim = forms.DateField(label = 'Até:')
    fim.widget.attrs = {'class' : 'form-control', 'placeholder' : 'Selecione a data'}

    congregacao = forms.ModelMultipleChoiceField(label = 'Congregações', required = False, queryset = Congregacao.objects.all().order_by('nome'), to_field_name = 'nome')
    congregacao.widget.attrs = {'class' : 'form-control', 'title' : 'Nenhuma selecionada'}

    forma = forms.ModelMultipleChoiceField(label = 'Formas de Entrada', required = False, queryset = Pagamento.objects.all().order_by('nome'), to_field_name = 'nome')
    forma.widget.attrs = {'class' : 'form-control', 'title' : 'Nenhuma selecionada'}
    
    categoria_entrada = forms.ModelMultipleChoiceField(label = 'Categorias de Entrada', required = False, queryset = CategoriaEntrada.objects.all().order_by('nome'), to_field_name = 'nome')
    categoria_entrada.widget.attrs = {'class' : 'form-control', 'title' : 'Nenhuma selecionada'}

    categoria_saida = forms.ModelMultipleChoiceField(label = 'Categorias de Saídas', required = False, queryset = CategoriaSaida.objects.all().order_by('nome'), to_field_name = 'nome')
    categoria_saida.widget.attrs = {'class' : 'form-control', 'title' : 'Nenhuma selecionada'}

    empresa = forms.ModelMultipleChoiceField(label = 'Empresas', required = False, queryset = Empresa.objects.all().order_by('nome'), to_field_name = 'nome')
    empresa.widget.attrs = {'class' : 'form-control', 'title' : 'Nenhuma selecionada'}

    membro = forms.ModelMultipleChoiceField(label = 'Membros', required = False, queryset = Membro.objects.all().order_by('nome'), to_field_name = 'nome')
    membro.widget.attrs = {'class' : 'form-control', 'title' : 'Nenhum selecionado'}

class SaidaForm(forms.Form):
    congregacao = forms.ModelChoiceField(label = 'Congregação', help_text = 'location_city', queryset = Congregacao.objects.all().order_by('nome'), empty_label = 'Nenhuma selecionada')
    congregacao.widget.attrs = {'class' : 'form-control'}

    categoria = forms.ModelChoiceField(label = 'Categoria', help_text = 'category', queryset = CategoriaSaida.objects.all().order_by('nome'), empty_label = 'Nenhuma selecionada')
    categoria.widget.attrs = {'class' : 'form-control'}

    pagamento = forms.ModelChoiceField(label = 'Forma de Pagamento', help_text = 'credit_card', queryset = Pagamento.objects.all().order_by('nome'), empty_label = 'Nenhuma selecionada')
    pagamento.widget.attrs = {'class' : 'form-control'}

    empresa = forms.ModelChoiceField(label = 'Empresa/Trabalhador', help_text = 'store', queryset = Empresa.objects.all().order_by('nome'), empty_label = 'Nenhum selecionado')
    empresa.widget.attrs = {'class' : 'form-control'}

    nome = forms.CharField(label = 'Nome', help_text = 'shopping_bag', max_length = 75)
    nome.widget.attrs = {'class' : 'form-control', 'placeholder' : 'Nome do produto ou serviço', 'autocomplete' : 'off'}
    
    descricao = forms.CharField(label = 'Descrição', help_text = 'short_text', required = False, max_length = 100)
    descricao.widget.attrs = {'class' : 'form-control', 'placeholder' : 'Descrição breve do produto ou serviço', 'autocomplete' : 'off'}

    valor = forms.DecimalField(label = 'Valor (R$)', help_text = 'monetization_on', min_value = 0, max_digits = 12, decimal_places = 2)
    valor.widget.attrs = {'class' : 'form-control', 'placeholder' : 'Valor do produto ou serviço'}

    data = forms.DateField(label = 'Data', help_text = 'event')
    data.widget.attrs = {'class' : 'form-control datepicker', 'placeholder' : 'Data que foi realizado o pagamento', 'format' : '%d/%m/%Y'}

    comprovante = forms.FileField(label = 'Comprovante', help_text = 'receipt', required = False)
    comprovante.widget.attrs = {'accept' : '.jpg, .jpeg, .png, .pdf'}

    nota_fiscal = forms.FileField(label = 'Nota Fiscal', help_text = 'sticky_note_2', required = False)
    nota_fiscal.widget.attrs = {'accept' : '.jpg, .jpeg, .png, .pdf'}

    class Meta:
        model = Saida
        fields = '__all__'