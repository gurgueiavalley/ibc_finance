from django import forms
from .models import *

class CategoriaForm(forms.Form):
    nome = forms.CharField(label = 'Nome', help_text = 'category', max_length = 30)
    nome.widget.attrs = {'class' : 'form-control', 'placeholder' : 'Nome da categoria', 'autocomplete' : 'off', 'maxlength' : '30'}   

class CongregacaoForm(forms.Form):
    nome = forms.CharField(label = 'Nome', help_text = 'location_city', max_length = 70)
    nome.widget.attrs = {'class' : 'form-control', 'placeholder' : 'Nome da congregação', 'autocomplete' : 'off', 'maxlength' : '70'}

class FornecedorForm(forms.Form):
    documento = forms.CharField(label = 'CPF/CNPJ', help_text = 'fingerprint', max_length = 15)
    documento.widget.attrs = {'class' : 'form-control', 'placeholder' : 'Número do CPF/CNPJ do fornecedor', 'autocomplete' : 'off', 'maxlength' : '15'}

    nome = forms.CharField(label = 'Nome', help_text = 'perm_identity', max_length = 70)
    nome.widget.attrs = {'class' : 'form-control', 'placeholder' : 'Nome do fornecedor', 'autocomplete' : 'off', 'maxlength' : '70'}

    descricao = forms.CharField(label = 'Descrição', help_text = 'short_text', max_length = 100, required = False)
    descricao.widget.attrs = {'class' : 'form-control', 'placeholder' : 'Descrição breve dos produtos/serviços do fornecedor', 'autocomplete' : 'off', 'maxlength' : '100'}

    endereco = forms.CharField(label = 'Endereço', help_text = 'location_on', max_length = 100, required = False)
    endereco.widget.attrs = {'class' : 'form-control', 'placeholder' : 'Nome da rua, número e/ou bairro', 'autocomplete' : 'off', 'maxlength' : '100'}

class EntradaForm(forms.Form):
    congregacao = forms.ModelChoiceField(label = 'Congregação', help_text = 'location_city', queryset = Congregacao.objects.all().order_by('nome'), empty_label = 'Nenhuma selecionada')
    congregacao.widget.attrs = {'class' : 'form-control'}

    categoria = forms.ModelChoiceField(label = 'Categoria', help_text = 'category', queryset = Categoria.objects.filter(tipo = 'ENTRADA').order_by('nome'), empty_label = 'Nenhuma selecionada')
    categoria.widget.attrs = {'class' : 'form-control'}

    transacao = forms.ModelChoiceField(label = 'Forma de Entrada', help_text = 'credit_card', queryset = Transacao.objects.all().order_by('nome'), empty_label = 'Nenhuma selecionada')
    transacao.widget.attrs = {'class' : 'form-control'}

    membro = forms.ModelChoiceField(label = 'Membro', help_text = 'person', queryset = Membro.objects.all().order_by('nome'), empty_label = 'Nenhum selecionado', required = False)
    membro.widget.attrs = {'class' : 'form-control'}

    anotacao = forms.CharField(label = 'Anotação', help_text = 'short_text', max_length = 100, required = False)
    anotacao.widget.attrs = {'class' : 'form-control', 'placeholder' : 'Detalhe ou descrição breve da entrada', 'autocomplete' : 'off', 'maxlenght' : '100'}

    valor = forms.DecimalField(label = 'Valor (R$)', help_text = 'monetization_on', max_digits = 12, decimal_places = 2)
    valor.widget.attrs = {'class' : 'form-control', 'autocomplete' : 'off', 'placeholder' : 'Valor da entrada', 'min' : '0', 'step' : '0.01'}

    data = forms.DateField(label = 'Data', help_text = 'event')
    data.widget.attrs = {'class' : 'form-control datepicker', 'placeholder' : 'Data que foi recebido a entrada'}

    comprovante = forms.FileField(label = 'Comprovante', help_text = 'receipt', required = False)
    comprovante.widget.attrs = {'accept' : '.jpg, .jpeg, .png, .pdf'}

    deletar = forms.BooleanField(label = 'Deletar o Atual', required = False)

class EntradaAvulsaForm(forms.Form):
    congregacao = forms.ModelChoiceField(label = 'Congregação', help_text = 'location_city', queryset = Congregacao.objects.all().order_by('nome'), empty_label = 'Nenhuma selecionada')
    congregacao.widget.attrs = {'class' : 'form-control'}

    transacao = forms.ModelChoiceField(label = 'Forma de Entrada', help_text = 'credit_card', queryset = Transacao.objects.all().order_by('nome'), empty_label = 'Nenhuma selecionada')
    transacao.widget.attrs = {'class' : 'form-control'}

    descricao = forms.CharField(label = 'Anotação', help_text = 'short_text', max_length = 100, required = False)
    descricao.widget.attrs = {'class' : 'form-control', 'placeholder' : 'Detalhe ou descrição breve da entrada', 'autocomplete' : 'off', 'maxlenght' : '100'}

    valor = forms.DecimalField(label = 'Valor (R$)', help_text = 'monetization_on', max_digits = 12, decimal_places = 2)
    valor.widget.attrs = {'class' : 'form-control', 'autocomplete' : 'off', 'placeholder' : 'Valor da entrada', 'min' : '0', 'step' : '0.01'}

    data = forms.DateField(label = 'Data', help_text = 'event')
    data.widget.attrs = {'class' : 'form-control datepicker', 'placeholder' : 'Data que foi recebido a entrada'}

    comprovante = forms.FileField(label = 'Comprovante', help_text = 'receipt', required = False)
    comprovante.widget.attrs = {'accept' : '.jpg, .jpeg, .png, .pdf'}

    deletar = forms.BooleanField(label = 'Deletar o Atual', required = False)

class EntradaMissaoForm(forms.Form):
    missao = forms.ModelChoiceField(label = 'Missão', help_text = 'feedback', queryset = Missao.objects.all().order_by('nome'), empty_label = 'Nenhuma selecionada')
    missao.widget.attrs = {'class' : 'form-control'}

    transacao = forms.ModelChoiceField(label = 'Forma de Entrada', help_text = 'credit_card', queryset = Transacao.objects.all().order_by('nome'), empty_label = 'Nenhuma selecionada')
    transacao.widget.attrs = {'class' : 'form-control'}

    valor = forms.DecimalField(label = 'Valor (R$)', help_text = 'monetization_on', max_digits = 12, decimal_places = 2)
    valor.widget.attrs = {'class' : 'form-control', 'autocomplete' : 'off', 'placeholder' : 'Valor da entrada', 'min' : '0', 'step' : '0.01'}

    data = forms.DateField(label = 'Data', help_text = 'event')
    data.widget.attrs = {'class' : 'form-control datepicker', 'placeholder' : 'Data que foi recebido a entrada'}

    anotacao = forms.CharField(label = 'Anotação', help_text = 'short_text', max_length = 100, required = False)
    anotacao.widget.attrs = {'class' : 'form-control', 'placeholder' : 'Detalhe ou descrição breve da entrada', 'autocomplete' : 'off', 'maxlenght' : '100'}

    comprovante = forms.FileField(label = 'Comprovante', help_text = 'receipt', required = False)
    comprovante.widget.attrs = {'accept' : '.jpg, .jpeg, .png, .pdf'}

    deletar = forms.BooleanField(label = 'Deletar o Atual', required = False)
   
class MembroForm(forms.Form):
    SEXOS = (
        (None, 'NENHUM SELECIONADO'),
        ('MASCULINO', 'MASCULINO'),
        ('FEMININO', 'FEMININO')
    )

    CPF = forms.CharField(label = 'CPF', help_text = 'fingerprint', max_length = 14, required = False)
    CPF.widget.attrs = {'class' : 'form-control', 'placeholder' : '000.000.000-00', 'autocomplete' : 'off', 'minlength' : '14', 'maxlength' : '14'}

    nome = forms.CharField(label = 'Nome', help_text = 'perm_identity', max_length = 75)
    nome.widget.attrs = {'class' : 'form-control', 'placeholder' : 'Nome do membro', 'autocomplete' : 'off', 'maxlength' : '75'}

    sexo = forms.ChoiceField(label = 'Sexo', help_text = 'male', choices = SEXOS, required = False)
    sexo.widget.attrs = {'class' : 'form-control'}

    nascimento = forms.DateField(label = 'Data de Nascimento', help_text = 'event', required = False)
    nascimento.widget.attrs = {'class' : 'form-control datepicker', 'placeholder' : '__/__/____'}

    celular = forms.CharField(label = 'Celular', help_text = 'smartphone', max_length = 14, required = False)
    celular.widget.attrs = {'class' : 'form-control', 'placeholder' : '00 0 0000-0000', 'autocomplete' : 'off', 'minlength' : '14' , 'maxlength' : '14'}

    email = forms.EmailField(label = 'E-mail', help_text = 'mail', max_length = 45, required = False)
    email.widget.attrs = {'class' : 'form-control', 'placeholder' : 'exemplo@exemplo.exemplo', 'autocomplete' : 'off', 'maxlength' : '50'}

class MissaoForm(forms.Form):
    congregacao = forms.ModelChoiceField(label = 'Congregação', help_text = 'location_city', queryset = Congregacao.objects.all().order_by('nome'), empty_label = 'Nenhuma selecionada')
    congregacao.widget.attrs = {'class' : 'form-control'}

    nome = forms.CharField(label = 'Nome', help_text = 'feedback', max_length = 50)
    nome.widget.attrs = {'class' : 'form-control', 'placeholder' : 'Nome da missão', 'autocomplete' : 'off', 'maxlength' : '50'}

    detalhe = forms.CharField(label = 'Descrição', help_text = 'short_text', max_length = 100, required = False)
    detalhe.widget.attrs = {'class' : 'form-control', 'placeholder' : 'Detalhe do objetivo da missão', 'autocomplete' : 'off', 'maxlength' : '100'}

    inicio = forms.DateField(label = 'Início', help_text = 'today')
    inicio.widget.attrs = {'class' : 'form-control datepicker', 'placeholder' : 'Data do começo da missão'}

    fim = forms.DateField(label = 'Fim', help_text = 'event')
    fim.widget.attrs = {'class' : 'form-control datepicker', 'placeholder' : 'Data do fim da missão'}

    meta = forms.DecimalField(label = 'Meta (R$)', help_text = 'monetization_on', max_digits = 12, decimal_places = 3)
    meta.widget.attrs = {'class' : 'form-control', 'placeholder' : 'Valor esperado de arrecadação', 'autocomplete' : 'off', 'min' : '0', 'step' : '0.01'}

class TransacaoForm(forms.Form):
    nome = forms.CharField(label = 'Nome', help_text = 'credit_card', max_length = 25)
    nome.widget.attrs = {'class' : 'form-control', 'placeholder' : 'Nome da forma de pagamento', 'autocomplete' : 'off', 'maxlength' : '25'}

class RelatorioEntradaForm(forms.Form):
    inicio = forms.DateField(label = 'De:')
    inicio.widget.attrs = {'class' : 'form-control', 'placeholder' : 'Selecione a data', 'autocomplete' : 'off'}

    fim = forms.DateField(label = 'Até:')
    fim.widget.attrs = {'class' : 'form-control', 'placeholder' : 'Selecione a data', 'autocomplete' : 'off'}

    congregacao = forms.ModelMultipleChoiceField(label = 'Congregações', required = False, queryset = Congregacao.objects.all().order_by('nome'), to_field_name = 'nome')
    congregacao.widget.attrs = {'class' : 'form-control', 'title' : 'Nenhuma selecionada'}

    categoria_entrada = forms.ModelMultipleChoiceField(label = 'Categorias', required = False, queryset = Categoria.objects.filter(tipo = 'ENTRADA').order_by('nome'), to_field_name = 'nome')
    categoria_entrada.widget.attrs = {'class' : 'form-control', 'title' : 'Nenhuma selecionada'}

    forma = forms.ModelMultipleChoiceField(label = 'Formas de Entrada', required = False, queryset = Transacao.objects.all().order_by('nome'), to_field_name = 'nome')
    forma.widget.attrs = {'class' : 'form-control', 'title' : 'Nenhuma selecionada'}

    membro = forms.ModelMultipleChoiceField(label = 'Membros', required = False, queryset = Membro.objects.all().order_by('nome'), to_field_name = 'nome')
    membro.widget.attrs = {'class' : 'form-control', 'title' : 'Nenhum selecionado'}

class RelatorioMissaoForm(forms.Form):
    inicio = forms.DateField(label = 'De:')
    inicio.widget.attrs = {'class' : 'form-control', 'placeholder' : 'Selecione a data', 'autocomplete' : 'off'}

    fim = forms.DateField(label = 'Até:')
    fim.widget.attrs = {'class' : 'form-control', 'placeholder' : 'Selecione a data', 'autocomplete' : 'off'}

    congregacao = forms.ModelMultipleChoiceField(label = 'Congregações', required = False, queryset = Congregacao.objects.all().order_by('nome'), to_field_name = 'nome')
    congregacao.widget.attrs = {'class' : 'form-control', 'title' : 'Nenhuma selecionada'}

    missao = forms.ModelMultipleChoiceField(label = 'Missões', required = False, queryset = Missao.objects.all().order_by('nome'), to_field_name = 'nome')
    missao.widget.attrs = {'class' : 'form-control', 'title' : 'Nenhuma selecionada'}

class RelatorioSaidaForm(forms.Form):
    inicio = forms.DateField(label = 'De:')
    inicio.widget.attrs = {'class' : 'form-control', 'placeholder' : 'Selecione a data', 'autocomplete' : 'off'}

    fim = forms.DateField(label = 'Até:')
    fim.widget.attrs = {'class' : 'form-control', 'placeholder' : 'Selecione a data', 'autocomplete' : 'off'}

    congregacao = forms.ModelMultipleChoiceField(label = 'Congregações', required = False, queryset = Congregacao.objects.all().order_by('nome'), to_field_name = 'nome')
    congregacao.widget.attrs = {'class' : 'form-control', 'title' : 'Nenhuma selecionada'}

    categoria_saida = forms.ModelMultipleChoiceField(label = 'Categorias', required = False, queryset = Categoria.objects.filter(tipo = 'SAÍDA').order_by('nome'), to_field_name = 'nome')
    categoria_saida.widget.attrs = {'class' : 'form-control', 'title' : 'Nenhuma selecionada'}

    pagamento = forms.ModelMultipleChoiceField(label = 'Formas de Pagamento', required = False, queryset = Transacao.objects.all().order_by('nome'), to_field_name = 'nome')
    pagamento.widget.attrs = {'class' : 'form-control', 'title' : 'Nenhuma selecionada'}

    empresa = forms.ModelMultipleChoiceField(label = 'Empresas', required = False, queryset = Fornecedor.objects.all().order_by('nome'), to_field_name = 'nome')
    empresa.widget.attrs = {'class' : 'form-control', 'title' : 'Nenhuma selecionada'}

class RelatorioGeralForm(forms.Form):
    inicio = forms.DateField(label = 'De:')
    inicio.widget.attrs = {'class' : 'form-control', 'placeholder' : 'Selecione a data', 'autocomplete' : 'off'}

    fim = forms.DateField(label = 'Até:')
    fim.widget.attrs = {'class' : 'form-control', 'placeholder' : 'Selecione a data', 'autocomplete' : 'off'}

    congregacao = forms.ModelMultipleChoiceField(label = 'Congregações', required = False, queryset = Congregacao.objects.all().order_by('nome'), to_field_name = 'nome')
    congregacao.widget.attrs = {'class' : 'form-control', 'title' : 'Nenhuma selecionada'}

    forma = forms.ModelMultipleChoiceField(label = 'Formas de Entrada', required = False, queryset = Transacao.objects.all().order_by('nome'), to_field_name = 'nome')
    forma.widget.attrs = {'class' : 'form-control', 'title' : 'Nenhuma selecionada'}
    
    categoria_entrada = forms.ModelMultipleChoiceField(label = 'Categorias de Entrada', required = False, queryset = Categoria.objects.filter(tipo = 'ENTRADA').order_by('nome'), to_field_name = 'nome')
    categoria_entrada.widget.attrs = {'class' : 'form-control', 'title' : 'Nenhuma selecionada'}

    categoria_saida = forms.ModelMultipleChoiceField(label = 'Categorias de Saídas', required = False, queryset = Categoria.objects.filter(tipo = 'SAÍDA').order_by('nome'), to_field_name = 'nome')
    categoria_saida.widget.attrs = {'class' : 'form-control', 'title' : 'Nenhuma selecionada'}

    empresa = forms.ModelMultipleChoiceField(label = 'Empresas', required = False, queryset = Fornecedor.objects.all().order_by('nome'), to_field_name = 'nome')
    empresa.widget.attrs = {'class' : 'form-control', 'title' : 'Nenhuma selecionada'}

    membro = forms.ModelMultipleChoiceField(label = 'Membros', required = False, queryset = Membro.objects.all().order_by('nome'), to_field_name = 'nome')
    membro.widget.attrs = {'class' : 'form-control', 'title' : 'Nenhum selecionado'}

class SaidaForm(forms.Form):
    congregacao = forms.ModelChoiceField(label = 'Congregação', help_text = 'location_city', queryset = Congregacao.objects.all().order_by('nome'), empty_label = 'Nenhuma selecionada')
    congregacao.widget.attrs = {'class' : 'form-control'}

    categoria = forms.ModelChoiceField(label = 'Categoria', help_text = 'category', queryset = Categoria.objects.filter(tipo = 'SAÍDA').order_by('nome'), empty_label = 'Nenhuma selecionada')
    categoria.widget.attrs = {'class' : 'form-control'}

    transacao = forms.ModelChoiceField(label = 'Forma de Pagamento', help_text = 'credit_card', queryset = Transacao.objects.all().order_by('nome'), empty_label = 'Nenhuma selecionada')
    transacao.widget.attrs = {'class' : 'form-control'}

    fornecedor = forms.ModelChoiceField(label = 'Fornecedor', help_text = 'store', queryset = Fornecedor.objects.all().order_by('nome'), empty_label = 'Nenhum selecionado')
    fornecedor.widget.attrs = {'class' : 'form-control'}

    nome = forms.CharField(label = 'Nome', help_text = 'shopping_bag', max_length = 35)
    nome.widget.attrs = {'class' : 'form-control', 'placeholder' : 'Nome do produto ou serviço', 'autocomplete' : 'off'}
    
    descricao = forms.CharField(label = 'Descrição', help_text = 'short_text', required = False, max_length = 100)
    descricao.widget.attrs = {'class' : 'form-control', 'placeholder' : 'Descrição breve do produto ou serviço', 'autocomplete' : 'off'}

    valor = forms.DecimalField(label = 'Valor (R$)', help_text = 'monetization_on', max_digits = 12, decimal_places = 2)
    valor.widget.attrs = {'class' : 'form-control', 'placeholder' : 'Valor do produto ou serviço', 'min' : '0', 'step' : '0.01', 'autocomplete' : 'off'}

    data = forms.DateField(label = 'Data', help_text = 'event')
    data.widget.attrs = {'class' : 'form-control datepicker', 'placeholder' : 'Data que foi realizado o pagamento', 'format' : '%d/%m/%Y'}

    comprovante = forms.FileField(label = 'Comprovante', help_text = 'receipt', required = False)
    comprovante.widget.attrs = {'accept' : '.jpg, .jpeg, .png, .pdf'}

    nota_fiscal = forms.FileField(label = 'Nota Fiscal', help_text = 'sticky_note_2', required = False)
    nota_fiscal.widget.attrs = {'accept' : '.jpg, .jpeg, .png'}

    deletar = forms.BooleanField(label = 'Deletar o Atual', required = False)
    deletar2 = forms.BooleanField(label = 'Deletar o Atual', required = False)

class UsuarioForm(forms.Form):
    nome = forms.CharField(label = 'Nome', help_text = 'shopping_bag', max_length = 50)
    nome.widget.attrs = {'class' : 'form-control', 'placeholder' : 'Nome do usuário', 'autocomplete' : 'off'}

    sobrenome = forms.CharField(label = 'Sobrenome', help_text = 'shopping_bag', max_length = 50)
    sobrenome.widget.attrs = {'class' : 'form-control', 'placeholder' : 'Sobrenome do usuário', 'autocomplete' : 'off'}

    email = forms.EmailField(label = 'E-mail', help_text = 'mail', max_length = 45, required = False)
    email.widget.attrs = {'class' : 'form-control', 'placeholder' : 'exemplo@exemplo.exemplo', 'autocomplete' : 'off', 'maxlength' : '50'}

    usuario = forms.CharField(label = 'Usuario', help_text = 'shopping_bag', max_length = 50)
    usuario.widget.attrs = {'class' : 'form-control', 'placeholder' : 'Usuário para login', 'autocomplete' : 'off'}

    ativo = forms.BooleanField(label = 'Ativo', required = False)