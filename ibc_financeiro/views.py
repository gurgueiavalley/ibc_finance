from django.shortcuts   import render
from .forms             import MemberForm

from django.contrib.auth    import authenticate, login, logout
from django.contrib         import messages
from django.shortcuts       import redirect

from .functions.fields import Money

from .models import *
from .forms import *
from django.contrib.auth.models import User

import pandas
from decimal import Decimal
import os
from datetime import datetime, date, timedelta
from reportlab.pdfgen import canvas
from django.conf import settings
from pathlib import Path
from itertools import chain                     # Juntar duas listas de queryset de classes diferentes
from reportlab.platypus import Table

from django.core.files.storage import default_storage
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

from .functions.report import *
from .functions.file    import *

from django.db.models import Sum
from django.urls import reverse

def conta(request, acao):
    if acao == 'login':
        if request.method == 'POST':
            user = authenticate(username = request.POST['username'], password = request.POST['password'])
            
            if user != None:
                if user.is_active:
                    login(request, user)
                    
                    return redirect('index')
            
            else:
                messages.error(request, 'Dados incorretos ou conta desativada')
        
        return render(request, 'financeiro/paginas/conta/login.html', {'inputs' : LoginForm()})
    
    elif acao == 'logout':
        logout(request)

        return redirect('index')
    
    else:
        return redirect('index')

@login_required(login_url='/conta/login')
def avulso(request, acao):
    if acao == 'alterar':
        entrada = EntradaAvulsa.objects.get(id = request.GET.get('id'))
        
        if request.method == 'POST':
            formulario = EntradaAvulsaForm(request.POST, request.FILES)
            
            if formulario.is_valid():
                entrada.congregacao = Congregacao.objects.get(id = request.POST['congregacao'])
                entrada.data = convertDate(request.POST['data'])
                
                entrada.transacao = Transacao.objects.get(id = request.POST['transacao'])
                
                entrada.anotacao = request.POST['descricao']
                entrada.valor = request.POST['valor']

                if 'comprovante' in request.FILES:
                    entrada.comprovante = request.FILES['comprovante']

                if 'deletar' in request.POST:
                    entrada.comprovante = None

                entrada.save()
                messages.success(request, "ALTERADO COM SUCESSO!")

        return render(request, 'financeiro/paginas/avulso/alterar.html', {'formulario' : EntradaAvulsaForm(), 'dados' : entrada})
    
    if request.method == 'POST':
        formulario = EntradaAvulsaForm(request.POST)

        if formulario.is_valid():
            entrada = EntradaAvulsa()
            entrada.congregacao = Congregacao.objects.get(id = request.POST['congregacao'])
            entrada.data = convertDate(request.POST['data'])
            entrada.transacao = Transacao.objects.get(id = request.POST['transacao'])

            if 'descricao' in request.POST:
                entrada.anotacao = request.POST['descricao']

            entrada.valor = request.POST['valor']

            if 'comprovante' in request.FILES:
                entrada.comprovante = request.FILES['comprovante']

            entrada.usuario = User.objects.get(id = request.user.id)

            entrada.save()
            messages.success(request, "ADICIONADO COM SUCESSO!")
    if acao == 'listar':
        tipo = 'avulso'
        return render(request, 'financeiro/paginas/form_listar.html', {'title': tipo,'formulario' : RelatorioEntradaForm()})
    return render(request, 'financeiro/paginas/avulso/adicionar.html', {'formulario' : EntradaAvulsaForm()})

@login_required(login_url='/conta/login')
def categoria(request, acao):
    if acao == "listar":
        categorias = Categoria.objects.filter(tipo = 'SAÍDA')
        return render(request, 'financeiro/paginas/categoria/tabela.html', {'categorias': categorias})

    if acao == "alterar":
        categoria = Categoria.objects.get(id = request.GET.get('id'))
        if request.method == 'POST':
            categoria.nome = request.POST['nome']
            categoria.save()
            
            messages.success(request,
                f'A categoria de saída <strong> { categoria.nome } </strong> foi alterada',
                extra_tags = '<strong> Categoria Atualizada </strong> <br>'
            )

            return redirect('/categoria/listar')
        return render(request, 'financeiro/paginas/categoria/alterar.html', {'formulario': CategoriaForm(), 'categoria': categoria})

    if acao == "deletar":
        categoria = Categoria.objects.get(id = request.GET.get('id'))
        if request.method == 'POST':
            name = categoria.nome

            categoria.delete()
            
            messages.success(request,
                f'A categoria de saída <strong> { name } </strong> foi excluída',
                extra_tags = '<strong> Categoria Deletada </strong> <br>'
            )

            return redirect('/categoria/listar')
        
        saidas = Saida.objects.filter(categoria__id=categoria.id)
        return render(request, 'financeiro/paginas/categoria/deletar.html', {'categoria': categoria,'saidas': saidas})

    pagina = 0

    if request.method == 'POST':
        formulario = CategoriaForm(request.POST)

        if formulario.is_valid():
            categoria = Categoria()
            categoria.nome = request.POST['nome']
            categoria.tipo = 'SAÍDA'
            
            categoria.save()
            messages.success(request, 'ADICIONADO COM SUCESSO!')
            pagina = 1
            
        return render(request, 'financeiro/paginas/categoria/adicionar.html', {'formulario' : CategoriaForm(), 'pagina' : pagina, 'id' : categoria.id, 'nome' : categoria.nome})
    if 'pop' in request.GET:
        return render(request, 'financeiro/paginas/categoria/adicionar.html', {'formulario' : CategoriaForm(),'pagina' : pagina, 'pop' : 'yes'})
    return render(request, 'financeiro/paginas/categoria/adicionar.html', {'formulario' : CategoriaForm(), 'pagina' : pagina})

@login_required(login_url='/conta/login')
def catEntrada(request, acao):
    
    if acao == "listar":
        categorias = Categoria.objects.filter(tipo = 'ENTRADA')
        return render(request, 'financeiro/paginas/catentrada/tabela.html', {'categorias': categorias})
    
    if acao == "alterar":
        categoria = Categoria.objects.get(id = request.GET.get('id'))
        if request.method == "POST":
            categoria.nome = request.POST['nome']
            categoria.save()
            
            messages.success(request,
                f'Categoria de entrada <strong> { categoria.nome } </strong> foi alterada',
                extra_tags = '<strong> Categoria Atualizada </strong> <br>'
            )

            return redirect('/catentrada/listar')
        return render(request, 'financeiro/paginas/catentrada/alterar.html', {'formulario': CategoriaForm(), 'categoria': categoria})

    if acao == "deletar":
        categoria = Categoria.objects.get(id = request.GET.get('id'))
        if request.method == 'POST':
            name = categoria.nome

            categoria.delete()
            
            messages.success(request,
                f'A categoria <strong> { name } </strong> foi excluída',
                extra_tags = '<strong> Categoria Deletada </strong> <br>'
            )

            return redirect('/catentrada/listar')
        
        entradas = Entrada.objects.filter(categoria__id=categoria.id)
        return render(request, 'financeiro/paginas/catentrada/deletar.html', {'categoria': categoria,'entradas': entradas})

    pagina = 0

    if request.method == 'POST':
        formulario = CategoriaForm(request.POST)

        if formulario.is_valid():
            categoria = Categoria()
            categoria.nome = request.POST['nome']
            categoria.tipo = 'ENTRADA'
        
            categoria.save()

            pagina = 1
            
        return render(request, 'financeiro/paginas/catentrada/adicionar.html', {'formulario' : CategoriaForm(), 'pagina' : pagina, 'id' : categoria.id, 'nome' : categoria.nome})

    if 'pop' in request.GET:
        return render(request, 'financeiro/paginas/catentrada/adicionar.html', {'formulario' : CategoriaForm(), 'pagina' : pagina, 'pop' : 'yes'})

    return render(request, 'financeiro/paginas/catentrada/adicionar.html', {'formulario' : CategoriaForm(), 'pagina' : pagina})

@login_required(login_url='/conta/login')
def congregacao(request, acao):
    if acao == "listar":
        congregacoes = Congregacao.objects.all()
        return render(request, 'financeiro/paginas/congregacao/tabela.html', {'congregacoes':congregacoes})
    
    if acao == "alterar":
        congregacao = Congregacao.objects.get(id = request.GET.get('id'))

        if request.method == 'POST':
            congregacao.nome = request.POST['nome']
            congregacao.save()
            messages.success(request, 'ALTERADO COM SUCESSO!')
            return redirect('/congregacao/listar')
        return render(request, 'financeiro/paginas/congregacao/alterar.html', {'formulario': CongregacaoForm(), 'congregacao': congregacao})

    pagina = 0

    congregacao = Congregacao()

    if request.method == 'POST':
        formulario = CongregacaoForm(request.POST)

        if formulario.is_valid():
            congregacao.nome = request.POST['nome']
            congregacao.save()

            pagina = 1

            messages.success(request, 'ADICIONADO COM SUCESSO!')

            return render(request, 'financeiro/paginas/congregacao/adicionar.html', {'formulario' : CongregacaoForm(), 'pagina' : pagina, 'id' : congregacao.id, 'nome' : request.POST['nome']})
    

    if 'pop' in request.GET:
        return render(request, 'financeiro/paginas/congregacao/adicionar.html', {'formulario' : CongregacaoForm(),'pagina' : pagina, 'pop' : 'yes'})

    return render(request, 'financeiro/paginas/congregacao/adicionar.html', {'formulario' : CongregacaoForm(),'pagina' : pagina})

@login_required(login_url='/conta/login')
def emissao(request, acao):
    if acao == 'listar':
        tipo = 'emissao'
        return render(request, 'financeiro/paginas/form_listar.html', {'title': tipo,'formulario' : RelatorioMissaoForm()})
    
    
    if acao == 'alterar':
        entrada = EntradaMissao.objects.get(id = request.GET.get('id'))
        
        if request.method == 'POST':
            formulario = EntradaMissaoForm(request.POST, request.FILES)
            
            if formulario.is_valid():
                entrada.missao = Missao.objects.get(id = request.POST['missao'])
                
                entrada.anotacao = request.POST['anotacao']

                entrada.transacao = Transacao.objects.get(id = request.POST['transacao'])
                entrada.valor = request.POST['valor']
                entrada.data = convertDate(request.POST['data'])

                if 'comprovante' in request.FILES:
                    entrada.comprovante = request.FILES['comprovante']

                if 'deletar' in request.POST:
                    entrada.comprovante = None

                entrada.save()
                messages.success(request, "ALTERADO COM SUCESSO!")
        return render(request, 'financeiro/paginas/emissao/alterar.html', {'formulario' : EntradaMissaoForm(), 'dados' : entrada})
    

    if request.method == 'POST':
        formulario = EntradaMissaoForm(request.POST)

        if formulario.is_valid():
            entrada = EntradaMissao()
            entrada.missao = Missao.objects.get(id = request.POST['missao'])
            entrada.transacao = Transacao.objects.get(id = request.POST['transacao'])
            entrada.usuario = User.objects.get(id = request.user.id)
            entrada.valor = request.POST['valor']
            entrada.data = convertDate(request.POST['data'])

            if 'anotacao' in request.POST:
                entrada.anotacao = request.POST['anotacao']

            if 'comprovante' in request.FILES:
                entrada.comprovante = request.FILES['comprovante']

            entrada.save()
            messages.success(request, "ADICIONADO COM SUCESSO!")

    return render(request, 'financeiro/paginas/emissao/adicionar.html', {'formulario' : EntradaMissaoForm()})

@login_required(login_url='/conta/login')
def empresa(request, acao):
    if acao == 'alterar':
        empresa = Fornecedor.objects.get(id = request.GET.get('id'))

        if request.method == 'POST':
            empresa.documento = request.POST['documento']
            empresa.nome = request.POST['nome']

            if 'descricao' in request.POST:
                empresa.descricao = request.POST['descricao']
            
            if 'endereco' in request.POST:
                empresa.endereco = request.POST['endereco']

            empresa.save()
            messages.success(request, "ALTERADO COM SUCESSO!")

            return redirect('/empresa/listar')
        return render(request, 'financeiro/paginas/empresa/alterar.html', {'formulario': FornecedorForm(), 'empresa': empresa})

    if acao == 'listar':
        empresas = Fornecedor.objects.all()
        return render(request, 'financeiro/paginas/empresa/tabela.html', {'empresas': empresas})
    
    pagina = 0

    if request.method == 'POST':
        formulario = FornecedorForm(request.POST)

        if formulario.is_valid():
            fornecedor = Fornecedor()
            fornecedor.documento = request.POST['documento']
            fornecedor.nome = request.POST['nome']
            
            if 'descricao' in request.POST:
                fornecedor.descricao = request.POST['descricao']
            
            if 'endereco' in request.POST:
                fornecedor.endereco = request.POST['endereco']

            fornecedor.save()

            pagina = 1

            messages.success(request, 'ADICIONADO COM SUCESSO!')
            
            return render(request, 'financeiro/paginas/empresa/adicionar.html', {'formulario' : FornecedorForm(), 'pagina' : pagina, 'id' : fornecedor.id, 'nome' : fornecedor.nome})
    
    if 'pop' in request.GET:
        return render(request, 'financeiro/paginas/empresa/adicionar.html', {'formulario' : FornecedorForm(), 'pagina' : pagina, 'pop' : 'yes'})

    return render(request, 'financeiro/paginas/empresa/adicionar.html', {'formulario' : FornecedorForm(), 'pagina' : pagina})

@login_required(login_url='/conta/login')
def entrada(request, acao):
    if acao == 'alterar':
        entrada = Entrada.objects.get(id = request.GET.get('id'))
        
        if request.method == 'POST':
            formulario = EntradaForm(request.POST, request.FILES)
            
            if formulario.is_valid():
                entrada.congregacao = Congregacao.objects.get(id = request.POST['congregacao'])
                entrada.categoria = Categoria.objects.get(id = request.POST['categoria'])
                entrada.transacao = Transacao.objects.get(id = request.POST['transacao'])
                entrada.membro = Membro.objects.get(id = request.POST['membro'])

                entrada.anotacao = request.POST['anotacao']
                entrada.valor = request.POST['valor']
                entrada.data = convertDate(request.POST['data'])

                if 'comprovante' in request.FILES:
                    entrada.comprovante = request.FILES['comprovante']

                if 'deletar' in request.POST:
                    entrada.comprovante = None

                entrada.save()
                messages.success(request, "ALTERADO COM SUCESSO!")

        return render(request, 'financeiro/paginas/entrada/alterar.html', {'formulario' : EntradaForm(), 'dados' : entrada})
    
    if request.method == 'POST':
        formulario = EntradaForm(request.POST)

        if formulario.is_valid():
            entrada = Entrada()
            entrada.congregacao = Congregacao.objects.get(id = request.POST['congregacao'])
            entrada.categoria = Categoria.objects.get(id = request.POST['categoria'])
            entrada.transacao = Transacao.objects.get(id = request.POST['transacao'])
            entrada.membro = Membro.objects.get(id = request.POST['membro'])

            if 'anotacao' in request.POST:
                entrada.anotacao = request.POST['anotacao']

            entrada.valor = request.POST['valor']
            entrada.data = convertDate(request.POST['data'])

            if 'comprovante' in request.FILES:
                entrada.comprovante = request.FILES['comprovante']

            entrada.usuario = User.objects.get(id = request.user.id)

            entrada.save()
            messages.success(request, "ADICIONADO COM SUCESSO!")
    if acao == 'listar':
        tipo = 'entradas'
        return render(request, 'financeiro/paginas/form_listar.html', {'title': tipo,'formulario' : RelatorioEntradaForm()})
    return render(request, 'financeiro/paginas/entrada/adicionar.html', {'formulario' : EntradaForm()})

@login_required(login_url = '/conta/login')
def index(request):
    ofertasMembros, ofertasAvulsas, ofertasMissoes = [], [], []
    hoje, antes = date.today(), date.today() - timedelta(days = 7)

    eMembro = Entrada.objects.filter(data__range = [antes, hoje]).order_by('data')
    eAvulsa = EntradaAvulsa.objects.filter(data__range = [antes, hoje]).order_by('data')
    eMissao = EntradaMissao.objects.filter(data__range = [antes, hoje]).order_by('data')

    for dia in range(0, 8):
        total = 0
        
        for entrada in eMembro:    
            if entrada.data == (hoje - timedelta(days = dia)):
                total += int(entrada.valor)

        ofertasMembros.append(total)

    for dia in range(0, 8):
        total = 0
        
        for entrada in eAvulsa:    
            if entrada.data == (hoje - timedelta(days = dia)):
                total += int(entrada.valor)

        ofertasAvulsas.append(total)

    for dia in range(0, 8):
        total = 0
        
        for entrada in eMissao:    
            if entrada.data == (hoje - timedelta(days = dia)):
                total += int(entrada.valor)

        ofertasMissoes.append(total)

    totalEntradas = int(Entrada.objects.filter(data__range = [antes, hoje]).aggregate(Sum('valor'))['valor__sum'] or 0)
    totalEntradas += int(EntradaAvulsa.objects.filter(data__range = [antes, hoje]).aggregate(Sum('valor'))['valor__sum'] or 0)
    totalEntradas += int(EntradaMissao.objects.filter(data__range = [antes, hoje]).aggregate(Sum('valor'))['valor__sum'] or 0)

    totalSaidas = int(Saida.objects.filter(data__range= [antes, hoje]).aggregate(Sum('valor'))['valor__sum'] or 0)

    saidas = Saida.objects.all().order_by('-data')[:5]

    dados = {
        'membros' : len(Membro.objects.all()),
        'congregacoes' : len(Congregacao.objects.all()),
        'missoes' : len(Missao.objects.filter(andamento = True)),
        'ofertasMembros' : ofertasMembros[::-1],
        'ofertasAvulsas' : ofertasAvulsas[::-1],
        'ofertasMissoes' : ofertasMissoes[::-1],
        'totalEntradas': totalEntradas,
        'totalSaidas' : totalSaidas,
        'saidas' : saidas
    }

    return render(request, 'financeiro/index.html', dados)

@login_required(login_url = '/conta/login')
def member(request, action):
    if action == 'adicionar':
        data = {
            'title' : 'Adicionar um Membro',
            'paths' : {
                'membros' : {
                    'icon' : 'people_alt',
                    'routes' : ['membros']
                },
                'adicionar' : {
                    'icon' : 'add'
                }
            },
            'form' : {
                'action' : action,
                'fields' : MemberForm,
                'divisions' : {
                    'dados' : {
                        'description' : f'Informe os dados para <strong> { action } </strong> o <strong> membro</strong>. Os que possuem <b> * </b> são <strong> obrigatórios </strong>',
                        'slice' : ':'
                    }
                },
                'buttons' : {
                    'adicionar' : {
                        'icon' : 'add',
                        'class' : 'float-left btn-success'
                    }
                }
            }
        }

        if request.method == 'POST':
            form = MemberForm(request.POST)
            
            if form.is_valid(): form.create(request, data)
            else: data['form']['fields'] = form

        return render(request, 'form.html', data)

@login_required(login_url='/conta/login')
def membro(request, acao):
    if acao == 'importar':            # Importar
        if request.method == 'POST':
            arquivo = request.FILES['file']

            nomeArquivo = default_storage.save('membros.' + arquivo.name.split('.')[-1], arquivo)
            
            planilha = pandas.read_excel(default_storage.open(nomeArquivo))

            for indice in range(len(planilha)):
                try:
                    Membro.objects.get(CPF = planilha['CPF'][indice])

                except:
                    membro = Membro()

                    membro.CPF = planilha['CPF'][indice]
                    membro.nome = planilha['NOME'][indice].upper()
                    membro.sexo = planilha['SEXO'][indice].upper()
                    # membro.nascimento = convertDate(planilha['NASCIMENTO'][indice])
                    membro.celular = planilha['CELULAR'][indice]
                    # membro.email = planilha['E-MAIL'][indice].upper()

                    # print(planilha['NASCIMENTO'][indice])

                    membro.save()

            os.remove(os.getcwd() + default_storage.url(nomeArquivo))
            messages.success(request, "IMPORTADO COM SUCESSO!")
            return render(request, 'financeiro/paginas/membro/tabela.html', {'membros' : Membro.objects.all().order_by('nome')})

        return render(request, 'financeiro/paginas/membro/importar.html')

    if acao == 'deletar':
        membro = Membro.objects.get(id=request.GET['id'])
        if request.method == 'POST':
            name = membro.nome

            membro.delete()
            
            messages.success(request,
                f'O membro <strong> { name } </strong> foi excluído',
                extra_tags = '<strong> Membro Deletado </strong> <br>'
            )
            return redirect('/listar/membros')
        else:
            entradas = Entrada.objects.filter(membro_id=membro.id)
            return render(request, 'financeiro/paginas/membro/deletar.html', {'membro': membro,'entradas': entradas})
    
    elif acao == 'alterar':
        membro = Membro.objects.get(id = request.GET.get('id'))

        if request.method == 'POST':
            formulario = MemberForm(request.POST)

            if formulario.is_valid():
                membro.CPF = request.POST['cpf']
                membro.nome = request.POST['name']
                membro.cell = request.POST['cell']
                membro.email = request.POST['email']
                membro.sex = request.POST['sex']
                membro.birth = convertDate(request.POST['birth']) if request.POST['birth'] != '' else None

                membro.save()
                
            messages.success(request,
                f'Os dados do membro <strong> { membro.nome } </strong> foram alterados',
                extra_tags = '<strong> Membro Atualizado </strong> <br>'
            )

            return redirect('/listar/membros')
        
        else:
            return render(request, 'financeiro/paginas/membro/alterar.html', {'formulario': MemberForm(), 'membro': membro})
    
    pagina = 0
    if request.method == 'POST':
        formulario = MembroForm(request.POST)

        if formulario.is_valid():
            membro = Membro()
            membro.CPF = request.POST['CPF']
            membro.nome = request.POST['nome']
            
            if 'celular' in request.POST:
                membro.celular = request.POST['celular']
            
            if 'email' in request.POST:
                membro.email = request.POST['email']
            
            if 'sexo' in request.POST:
                membro.sexo = request.POST['sexo']
            
            if 'nascimento' in request.POST:
                membro.nascimento = convertDate(request.POST['nascimento'])

            membro.save()
            messages.success(request, "ADICIONADO COM SUCESSO!")
            pagina = 1
            
        return render(request, 'financeiro/paginas/membro/adicionar.html', {'formulario' : MembroForm(), 'pagina' : pagina, 'id' : membro.id, 'nome' : membro.nome})

    if 'pop' in request.GET:
        return render(request, 'financeiro/paginas/membro/adicionar.html', {'formulario' : MembroForm(), 'pagina' : pagina, 'pop' : 'yes'})
        
    return render(request, 'financeiro/paginas/membro/adicionar.html', {'formulario' : MembroForm(), 'pagina' : pagina})

@login_required(login_url='/conta/login')
def usuario(request, acao):
    if acao == 'listar':
        #Listando todos os usuarios
        usuarios = User.objects.filter(is_superuser=False, is_staff = False).exclude(username=request.user.username)

        return render(request, 'financeiro/paginas/usuario/tabela.html', {'usuarios': usuarios})
    if acao == 'adicionar':
        #Adiciondo uma conta de usuario
        if request.method == 'POST':
            formulario = UsuarioForm(request.POST)
            if formulario.is_valid():
                #Verificando se já existe um usuario cadastrado com o mesmo username
                try:
                    usuario = User.objects.get(username=request.POST['usuario'], email=request.POST['email'])
                except ObjectDoesNotExist:
                    usuario = User.objects.create_user(request.POST['usuario'], request.POST['email'], request.POST['password'])
                    usuario.first_name = request.POST['nome']
                    usuario.last_name = request.POST['sobrenome']
                    if 'ativo' in request.POST:
                        usuario.is_active = True
                    else:
                        usuario.is_active = False
                    usuario.save()
                    messages.success(request, "ADICIONADO COM SUCESSO!")
                    return redirect('/usuario/listar')
                else:
                    alert = 'USUARIO JÁ FOI CADASTRADO!'
                    return render(request, 'financeiro/paginas/usuario/adicionar.html', {'formulario': UsuarioForm(), 'alert': alert})
        
        #Redirecionando para pagina de adição de usuario
        return render(request, 'financeiro/paginas/usuario/adicionar.html', {'formulario': UsuarioForm()})

    elif acao == 'alterar':
        usuario = User.objects.get(id = request.GET['id'])
        
        #Alterar situação do usuario (Ativar/ Desativar)
        if request.method == 'POST':
            if 'ativo' in request.POST:
                usuario.is_active = True
            else:
                usuario.is_active = False
            usuario.save()
            messages.success(request, "ALTERADO COM SUCESSO!")
            return redirect('/usuario/listar')          

        #redirecionando para pagina de visualização e alteração
        else:
            return render(request, 'financeiro/paginas/usuario/alterar.html', {'formulario': UsuarioForm(), 'usuario': usuario})

    elif acao == 'perfil':
        usuario = User.objects.get(id = request.user.id)
        
        #Alterando dados do perfil do usuario
        if request.method == 'POST':                
            usuario.first_name = request.POST['nome']
            usuario.last_name = request.POST['sobrenome']
            usuario.email = request.POST['email']
            usuario.username = request.POST['usuario']
            if 'ativo' in request.POST:
                usuario.is_active = True
            else:
                usuario.is_active = False
            usuario.save()
            messages.success(request, "ALTERADO COM SUCESSO!")
        
        # Redireciona para visualização e alteração dos dados do perfil
        return render(request, 'financeiro/paginas/usuario/perfil.html', {'formulario': UsuarioForm(), 'usuario': usuario})

    elif acao == 'alterarSenha':
        if request.method == 'POST':        # Alterando senha do usuário
            usuario = User.objects.get(id = request.user.id)
            
            if request.POST['password1'] == request.POST['password2']:
                usuario.set_password(request.POST['password1'])
                usuario.save()
                messages.success(request, "ALTERADO COM SUCESSO!")
                return render(request, 'financeiro/paginas/usuario/perfil.html', {'formulario': UsuarioForm(), 'usuario': usuario})
            else:
                alert = 'SENHAS NÃO CONFEREM!'
                return render(request, 'financeiro/paginas/usuario/alterar_senha.html', {'alert': alert})
        
        #redirecionando para formulario de alteração de senha
        return render(request, 'financeiro/paginas/usuario/alterar_senha.html')

@login_required(login_url='/conta/login')
def missao(request, acao):
    pagina = 0

    missao = Missao()
    
    if acao == "listar":
        missoes = Missao.objects.all()
        return render(request, 'financeiro/paginas/missao/tabela.html', {'missoes': missoes})

    if acao == "alterar":
        missao = Missao.objects.get(id = request.GET.get('id'))
        if request.method == "POST":
            formulario = MissaoForm(request.POST)
            if formulario.is_valid():
                missao.congregacao = Congregacao.objects.get(id = request.POST['congregacao'])
                missao.nome = request.POST['nome']
                missao.detalhe = request.POST['detalhe']
                missao.inicio = convertDate(request.POST['inicio'])
                missao.fim = convertDate(request.POST['fim'])
                missao.meta = request.POST['meta']
                if 'andamento' in request.POST:
                    missao.andamento = True
                else:
                    missao.andamento = False

                missao.save()
            messages.success(request, "ALTERADO COM SUCESSO!")
            return redirect('/missao/listar')
        return render(request, 'financeiro/paginas/missao/alterar.html', {'formulario': MissaoForm(),'missao': missao})

    if request.method == 'POST':
        formulario = MissaoForm(request.POST)

        if formulario.is_valid():
            missao.congregacao = Congregacao.objects.get(id = request.POST['congregacao'])
            missao.nome = request.POST['nome']
            
            if 'detalhe' in request.POST:
                missao.detalhe = request.POST['detalhe']

            missao.inicio = convertDate(request.POST['inicio'])
            missao.fim = convertDate(request.POST['fim'])
            missao.meta = request.POST['meta']
            missao.andamento = True

            missao.save()

            messages.success(request, "ADICIONADO COM SUCESSO!")
            
            pagina = 1

            return render(request, 'financeiro/paginas/missao/adicionar.html', {'formulario' : MissaoForm(), 'pagina' : pagina, 'id' : missao.id, 'nome' : request.POST['nome']})

    if 'pop' in request.GET:
        return render(request, 'financeiro/paginas/missao/adicionar.html', {'formulario' : MissaoForm(), 'pagina' : pagina, 'pop' : 'yes'})

    return render(request, 'financeiro/paginas/missao/adicionar.html', {'formulario' : MissaoForm(), 'pagina' : pagina})

@login_required(login_url='/conta/login')
def pagamento(request, acao):
    if acao == "listar":
        pagamentos = Transacao.objects.all()
        return render(request, 'financeiro/paginas/pagamento/tabela.html', {'pagamentos': pagamentos})
    
    if acao == "alterar":
        pagamento = Transacao.objects.get(id = request.GET.get('id'))
        if request.method == "POST":
            pagamento.nome = request.POST['nome']
            pagamento.save()
            
            messages.success(request,
                f'A forma de pagamento <strong> { pagamento.nome } </strong> foi atualizada',
                extra_tags = '<strong> Pagamento Atualizado </strong> <br>'
            )

            return redirect('/pagamento/listar')
        return render(request, 'financeiro/paginas/pagamento/alterar.html', {'formulario': TransacaoForm(), 'pagamento': pagamento})

    if acao == "deletar":
        pagamento = Transacao.objects.get(id = request.GET.get('id'))
        if request.method == 'POST':
            name = pagamento.nome

            pagamento.delete()
            
            messages.success(request,
                f'A forma de pagamento <strong> { name } </strong> foi excluída',
                extra_tags = '<strong> Pagamento Deletado </strong> <br>'
            )

            return redirect('/pagamento/listar')
        
        entradas = Entrada.objects.filter(transacao__id=pagamento.id)
        eavulsas = EntradaAvulsa.objects.filter(transacao__id=pagamento.id)
        emissoes = EntradaMissao.objects.filter(transacao__id=pagamento.id)
        saidas = Saida.objects.filter(transacao__id=pagamento.id)
        return render(request, 'financeiro/paginas/pagamento/deletar.html', {'pagamento': pagamento,'entradas': entradas, 'eavulsas': eavulsas, 'emissoes': emissoes, 'saidas': saidas}) 
    
    pagina = 0

    if request.method == 'POST':
        formulario = TransacaoForm(request.POST)

        if formulario.is_valid():
            transacao = Transacao()
            transacao.nome = request.POST['nome']
            transacao.save()

            pagina = 1
            
        return render(request, 'financeiro/paginas/pagamento/adicionar.html', {'formulario' : TransacaoForm(), 'pagina' : pagina, 'id' : transacao.id, 'nome' : transacao.nome})

    if 'pop' in request.GET:
        return render(request, 'financeiro/paginas/pagamento/adicionar.html', {'formulario' : TransacaoForm(), 'pagina' : pagina, 'pop' : 'yes'})

    return render(request, 'financeiro/paginas/pagamento/adicionar.html', {'formulario' : TransacaoForm(), 'pagina' : pagina})

@login_required(login_url='/conta/login')
def saida(request, acao):
    if acao == 'alterar':
        saida = Saida.objects.get(id = request.GET.get('id'))

        if request.method == 'POST':
            formulario = SaidaForm(request.POST)

            if formulario.is_valid():
                saida.congregacao = Congregacao.objects.get(id = request.POST['congregacao'])
                saida.categoria = Categoria.objects.get(id = request.POST['categoria'])
                saida.transacao = Transacao.objects.get(id = request.POST['transacao'])
                saida.fornecedor = Fornecedor.objects.get(id = request.POST['fornecedor'])
                saida.nome = request.POST['nome']
                saida.descricao = request.POST['descricao']
                saida.valor = request.POST['valor']
                saida.data = convertDate(request.POST['data'])

                if('comprovante' in request.FILES):
                    saida.comprovante = request.FILES['comprovante']

                if('deletar' in request.POST):
                    saida.comprovante = None

                if('nota_fiscal' in request.FILES):
                    saida.nf = request.FILES['nota_fiscal']

                if('deletar2' in request.POST):
                    saida.nf = None
                
                saida.usuario = User.objects.get(id = request.user.id)
                saida.save()
                messages.success(request, "ALTERADO COM SUCESSO!")
        return render(request, 'financeiro/paginas/saida/alterar.html', {'formulario': SaidaForm(), 'saida': saida})


    if(request.method == 'POST'):
        formulario = SaidaForm(request.POST, request.FILES)

        if formulario.is_valid():
            saida = Saida()
            saida.congregacao = Congregacao.objects.get(id = request.POST['congregacao'])
            saida.categoria = Categoria.objects.get(id = request.POST['categoria'])
            saida.transacao = Transacao.objects.get(id = request.POST['transacao'])
            saida.fornecedor = Fornecedor.objects.get(id = request.POST['fornecedor'])
            saida.nome = request.POST['nome']
            saida.descricao = request.POST['descricao']
            saida.valor = request.POST['valor']
            saida.data = convertDate(request.POST['data'])

            if('comprovante' in request.FILES):
                saida.comprovante = request.FILES['comprovante']

            if('nota_fiscal' in request.FILES):
                saida.nf = request.FILES['nota_fiscal']
            
            saida.usuario = User.objects.get(id = request.user.id)
            saida.save()
            messages.success(request, "ADICIONADO COM SUCESSO!")

    elif acao == 'listar':
        tipo = 'saídas'
        return render(request, 'financeiro/paginas/form_listar.html', {'title': tipo,'formulario' : RelatorioSaidaForm()})
    return render(request, 'financeiro/paginas/saida/adicionar.html', {'formulario' : SaidaForm()})

@login_required(login_url='/conta/login')
def listar(request, tipo):
    if tipo == 'saídas':
        saidas = listaSaida(request)
        return render(request, 'financeiro/paginas/saida/tabela.html', {'saidas' : saidas})

    elif tipo == 'entradas':
        entradas = []
        e = listaEntrada(request)
        for entrada in e:
            if hasattr(entrada, 'categoria'):
                entradas.append(entrada)
        return render(request, 'financeiro/paginas/entrada/tabela.html', {'entradas' : entradas})

    elif tipo == 'emissao':
        missoes = listaMissao(request)
        return render(request, 'financeiro/paginas/emissao/tabela.html', {'missoes' : missoes})

    elif tipo == 'membros':
        membros = Membro.objects.all()
        return render(request, 'financeiro/paginas/membro/tabela.html', {'membros' : membros})

    elif tipo == 'avulso':
        avulso = []
        e = listaEntrada(request)
        for entrada in e:
            if not hasattr(entrada, 'categoria'):
                avulso.append(entrada)
        return render(request, 'financeiro/paginas/avulso/tabela.html', {'avulso' : avulso})

def cabecalhoRelatorio(pdf, data):
    pdf.drawImage('ibc_financeiro/static/imagens/logo.jpg', 45, 740, 80, 80)    # Logo

    # Título
    pdf.setFont('Times-Bold', 16)
    pdf.drawString(205, 800, 'Igreja Batista de Corrente')
    
    # Subtítulos
    pdf.setFont('Times-Bold', 13)
    
    pdf.drawString(175, 785, 'Departamento de Administração e Finanças')
    pdf.drawString(data['subtitle']['x'], 770, f'Relatório Financeiro {data["subtitle"]["text"]}')
    
    pdf.drawString(200, 753, 'De:')
    pdf.drawString(309, 753, 'Até:')

    pdf.drawString(480, 785, 'Gerado Em')

    # Datas
    pdf.setFont('Times-Roman', 12)
    
    pdf.drawString(224, 753, data['dates']['init'])
    pdf.drawString(336, 753, data['dates']['end'])

    pdf.drawString(485, 771, f'{date.today().strftime("%d-%m-%Y")}')

def convertDate(date):
    return datetime.strptime(date, '%d/%m/%Y').date()

def gerarRelatorio(request, dados, tipo):
    y, total = 0, 0
    
    if tipo == 'entrada':
        directory = 'ibc_financeiro/static/entrada.pdf'
        pdf = canvas.Canvas(directory)

        cabecalhoRelatorio(pdf, {
            'subtitle' : {
                'x' : 200,
                'text' : 'das Entradas',
            },
            'dates' : {
                'init' : f'{request.POST["inicio"]}',
                'end' : f'{request.POST["fim"]}'
            }
        })

        pdf.setFont('Times-Bold', 13)

        pdf.drawString(20, 700, 'Data')
        pdf.drawString(100, 700, 'Congregação')
        pdf.drawString(330, 700, 'Categoria')
        pdf.drawString(490, 700, 'Valor')

        for entrada in dados:
            y = y + 30

            if(y > 580):
                y = 0

                pdf.showPage()

            pdf.setFont('Helvetica', 10)

            pdf.line(585, 718 - y, 10, 718 - y)

            pdf.drawString(20, 700 - y, str(entrada.data.strftime('%d/%m/%Y')))
            pdf.drawString(100, 700 - y, str(entrada.congregacao)[:35])
            pdf.drawString(330, 700 - y, str(entrada.categoria)[:25] if hasattr(entrada, 'categoria') else 'AVULSA')
            pdf.drawString(490, 700 - y, 'R$ ' + str(entrada.valor))
        
            total += entrada.valor
        
        pdf.line(585, 690 - y, 10, 690 - y)

        pdf.setFont('Times-Bold', 12)
        pdf.drawString(400, 650 - y, 'Total: R$ ' + str(total))

        pdf.save()

        if 'attachment' in request.POST:
            Report.receipt(dados, directory, 'ibc_financeiro/static/pdf/report/entry.pdf', 'Relatório de Entradas')

        else:
            return 'entrada.pdf'

    if tipo == 'saida':
        directory = 'ibc_financeiro/static/saida.pdf'
        pdf = canvas.Canvas(directory)
        
        cabecalhoRelatorio(pdf, {
            'subtitle' : {
                'x' : 205,
                'text' : 'das Saídas',
            },
            'dates' : {
                'init' : f'{request.POST["inicio"]}',
                'end' : f'{request.POST["fim"]}'
            }
        })

        pdf.setFont('Times-Bold', 13)

        pdf.drawString(20, 700, 'Data')
        pdf.drawString(100, 700, 'Congregação')
        pdf.drawString(330, 700, 'Categoria')
        pdf.drawString(490, 700, 'Valor')

        for saida in dados:
            y = y + 30

            if(y > 580):
                y = 0

                pdf.showPage()
            
            pdf.setFont('Helvetica', 10)
            
            pdf.line(585, 718 - y, 10, 718 - y)

            pdf.drawString(20, 700 - y, str(saida.data.strftime('%d/%m/%Y')))
            pdf.drawString(100, 700 - y, str(saida.congregacao)[:35])
            pdf.drawString(330, 700 - y, str(saida.categoria)[:25])
            pdf.drawString(490, 700 - y, 'R$ ' + str(saida.valor))
        
            total += saida.valor
        
        pdf.line(585, 690 - y, 10, 690 - y)

        pdf.setFont('Times-Bold', 12)
        pdf.drawString(400, 650 - y, 'Total: R$ ' + str(total))
        
        pdf.save()

        if 'attachment' in request.POST:
            Report.receipt(dados, directory, 'ibc_financeiro/static/pdf/report/exit.pdf', 'Relatório de Saídas')
    
        else:
            return 'saida.pdf'

    if tipo == 'missao':
        missions = []

        for entry in dados:
            mission = entry.missao.nome
            missions.append(mission) if mission not in missions else None

        directory = 'ibc_financeiro/static/missoes.pdf'
        pdf = canvas.Canvas(directory)

        cabecalhoRelatorio(pdf, {
            'subtitle' : {
                'x' : 205,
                'text' : 'de Missões',
            },
            'dates' : {
                'init' : f'{request.POST["inicio"]}',
                'end' : f'{request.POST["fim"]}'
            }
        })

        pdf.setFont('Times-Bold', 13)
        
        page = False

        for mission in missions:
            if page == False and y > 450:
                y, page = 0, True

                pdf.showPage()

            pdf.setFont('Times-Bold', 12)

            positionY = 750

            if page:
                if y > 550:
                    y = 0
                    
                    pdf.showPage()
                    pdf.setFont('Times-Bold', 12)

            else:
                positionY -= 65

            pdf.drawString(25, positionY - y, mission)
                
            positionY -= 50
            pdf.drawString(105, positionY - y, 'Data')
            pdf.drawString(305, positionY - y, 'Valor')
            
            positionY -= 5
            pdf.rect(100, positionY - y, 200, 30)
            pdf.rect(300, positionY - y, 200, 30)

            goal = 0

            for entry in dados:
                if entry.missao.nome == mission:
                    if page == False and y > 450:
                        y, page = 0, True

                        pdf.showPage()

                    pdf.setFont('Helvetica', 10)

                    positionY = 665

                    if page:
                        if y > 550:
                            y = 0
                            
                            pdf.showPage()
                            pdf.setFont('Helvetica', 10)

                    else:
                        positionY -= 65

                    pdf.rect(100, positionY - y, 200, 30)
                    pdf.rect(300, positionY - y, 200, 30)

                    positionY += 5
                    pdf.drawString(105, positionY - y, str(entry.data.strftime('%d/%m/%Y')))
                    pdf.drawString(305, positionY - y, 'R$ ' + str(entry.valor))

                    total += entry.valor
                    y += 30

                    goal = entry.missao.meta
            
            Chart.progress(pdf, goal, total, (670 if page else 600) - y)
            
            total = 0
            y += 150

        pdf.save()

        if 'attachment' in request.POST:
            Report.receipt(dados, directory, 'ibc_financeiro/static/pdf/report/missions.pdf', 'Relatório de Missões', {'pageLine' : ''})

        else:
            return 'missoes.pdf'

def gerarRelatorioGeral(request, entradas, saidas, missoes):
    directory = 'ibc_financeiro/static/general.pdf'
    pdf = canvas.Canvas(directory)

    cabecalhoRelatorio(pdf, {
        'subtitle' : {
            'x' : 218,
            'text' : 'Geral',
        },
        'dates' : {
            'init' : f'{request.POST["inicio"]}',
            'end' : f'{request.POST["fim"]}'
        }
    })
    
    categories, single = [], 0

    for entry in entradas:
        if hasattr(entry, 'categoria'):
            category = entry.categoria.nome
            categories.append(category) if category not in categories else None

        else:
            single += entry.valor
    
    mission = 0

    for m in missoes:
        mission += m.valor
    
    entrys, y, points = single + mission, 0, ''

    for repeat in range(100):
        points += '.'

    for category in categories:
        entrance = 0

        for entry in entradas:
            if hasattr(entry, 'categoria'):    
                entrance += entry.valor if entry.categoria.nome == category else 0
        
        entrys += entrance
        
        pdf.setFont('Helvetica', 10)

        pdf.drawString(50, 700 - y, category[:30] + points)
        pdf.drawString(365, 702 - y, 'R$ ' + str(entrance))
        pdf.line(363, 700.7 - y, 550, 700.7 - y) 
        
        y += 20
    
    pdf.drawString(50, 700 - y, 'OFERTAS AVULSAS' + points)
    pdf.drawString(365, 702 - y , 'R$ ' + str(single))
    pdf.line(363, 700.5 - y, 550, 700.5 - y)

    pdf.drawString(50, 678 - y , 'MISSÕES' + points) 
    pdf.drawString(365, 680 - y, 'R$ ' + str(mission))
    pdf.line(363, 678.5 - y, 550, 678.5 - y)

    pdf.setFont('Times-Bold', 12)
    pdf.drawString(320, 642 - y, 'Total:')
    pdf.line(363, 640 - y, 550, 640 - y)

    pdf.setFont('Helvetica', 10)
    pdf.drawString(365, 642 - y, 'R$ ' + str(entrys))

    # Exits
    pdf.setFont('Times-Bold', 13)

    pdf.drawString(160, 610 - y, f'{" Saídas ":-^58}')  # Title

    # Columns
    pdf.drawString(50, 583 - y, 'Nº')
    pdf.drawString(90, 583 - y, 'Nome')
    pdf.drawString(300, 583 - y, 'Data')
    pdf.drawString(385, 583 - y, 'Valor')

    total, page = 0, False

    # Walking through the exits
    for index in range(1, len(saidas) + 1):
        y += 17     # Space between lines

        # Second Page
        if page == False and y > 540:       # Limit of first page
            pdf.showPage()
            y, page = 0, True

        positionY = 750     # Beginning of other pages

        # Other Pages
        if page == True:
            if y > 700:
                pdf.showPage()
                y = 0

        else:   # First Page
            positionY = 580     # Beginning of first exit

        pdf.setFont('Helvetica', 11)
        i = index - 1

        pdf.drawString(50, positionY - y, f'{index}º')                                  # Line number
        pdf.drawString(90, positionY - y, f'{saidas[i]}'.title())                       # Name
        pdf.drawString(300, positionY - y, f'{saidas[i].data.strftime("%d/%m/%Y")}')    # Date
        pdf.drawString(385, positionY - y, Money().mask(f'{saidas[i].valor}'))          # Money

        total += saidas[index - 1].valor        # Somatory of Exits

    positionY = 720

    if page == True:    # Other Pages
        if y > 615:
            pdf.showPage()
            y = 0

    else:               # First page
        positionY = 540

    # Total
    pdf.setFont('Times-Bold', 13)
    pdf.drawString(385, positionY - y, 'Total')

    pdf.setFont('Helvetica', 11)
    pdf.drawString(385, positionY - (y + 15), Money().mask(f'{ total }'))
    
    # Signature
    positionY = 25

    pdf.setFont('Times-Bold', 13)
    pdf.drawString(20, positionY + 50, 'Conferido por')
    
    pdf.line(20,  positionY, 200, positionY)
    pdf.line(210, positionY, 400, positionY)
    pdf.line(410, positionY, 575, positionY)

    # Dízimos
    if 'dizimo' in request.POST:
        pdf.showPage()

        pdf.setFont('Times-Bold', 14)
        pdf.drawString(180, 750, 'IGREJA BATISTA DE CORRENTE')
        pdf.rect(20, 745, 553, 20)

        pdf.setFont('Helvetica', 10)
        pdf.drawString(230, 720, 'CONTROLE DE DÍZIMOS')
        pdf.drawString(219, 705, 'De: {} Até: {}'.format(request.POST['inicio'], request.POST['fim']))

        pdf.setFont('Helvetica-Bold', 10)

        pdf.drawString(180, 650, 'RELAÇÃO NOMINAL')
        pdf.rect(20, 645, 400, 20)
        
        pdf.drawString(435, 650, 'VALOR')
        pdf.rect(420, 645, 152, 20)

        y, entrance = 0, 0
        
        for entry in entradas:
            if hasattr(entry, 'categoria'):
                if entry.categoria.nome == 'DÍZIMO':
                    if y > 500:
                        y = 0
                        
                        pdf.showPage()

                    y += 20
                    entrance += entry.valor

                    pdf.setFont('Helvetica', 10)

                    pdf.drawString(35, 650 - y, str(entry.membro.nome))
                    pdf.rect(20, 645 - y, 400, 20)
                    
                    pdf.drawString(435, 650 - y, 'R$ ' + str(entry.valor))
                    pdf.rect(420, 645 - y, 152, 20)
        
        y += 20

        pdf.setFont('Helvetica-Bold', 10)
        pdf.drawString(370, 650 - y, 'TOTAL')
        pdf.rect(20, 645 - y, 400, 20)

        pdf.setFont('Helvetica', 10)
        pdf.drawString(435, 650 - y, 'R$ ' + str(entrance))
        pdf.rect(420, 645 - y, 152, 20)
    
    pdf.save()

    report = directory

    if 'chart' in request.POST:
        if saidas:
            Chart.pie(saidas)

            directories = [
                directory,
                'ibc_financeiro/static/chart.pdf'
            ]

            PDF.merge(directories, 'ibc_financeiro/static/general2.pdf')

            File.delete(directories)

            report = 'ibc_financeiro/static/general2.pdf'

    if 'attachment' in request.POST:
        Report.receipt(saidas, report, 'ibc_financeiro/static/pdf/report/general.pdf', 'Relatório Geral', {'page' : ''})

    else:
        return 'general2.pdf' if 'chart' in request.POST else 'general.pdf'

@login_required(login_url = '/conta/login')
def relatorio(request, tipo):
    if tipo == 'entrada':
        if request.method == 'POST':
            path = gerarRelatorio(request, listaEntrada(request), tipo) or 'pdf/report/entry.pdf'

            return render(request, 'financeiro/paginas/relatorio.html', {'nome': path, 'title' : 'de ' + tipo})

        return render(request, 'financeiro/paginas/relatorio.html', {'title' : tipo, 'formulario' : RelatorioEntradaForm()})

    elif tipo == 'saida':
        if request.method == 'POST':
            path = gerarRelatorio(request, listaSaida(request), tipo) or 'pdf/report/exit.pdf'

            return render(request, 'financeiro/paginas/relatorio.html', {'nome': path, 'title' : 'de ' + tipo})

        return render(request, 'financeiro/paginas/relatorio.html', {'title' : tipo, 'formulario' : RelatorioSaidaForm()})

    elif tipo == 'missao':
        if request.method == 'POST':
            path = gerarRelatorio(request, listaMissao(request), tipo) or 'pdf/report/missions.pdf'
            
            return render(request, 'financeiro/paginas/relatorio.html', {'nome': path, 'title' : 'de ' + tipo})
        
        return render(request, 'financeiro/paginas/relatorio.html', {'title' : tipo, 'formulario' : RelatorioMissaoForm()})

    elif tipo == 'geral':
        if request.method == 'POST':
            path = gerarRelatorioGeral(request, listaEntrada(request), listaSaida(request), listaMissao(request)) or 'pdf/report/general.pdf'
            
            return render(request, 'financeiro/paginas/relatorio.html', {'nome': path, 'title' : tipo})
        
        return render(request, 'financeiro/paginas/relatorio.html', {'title' : tipo, 'formulario' : RelatorioGeralForm()})

def listaEntrada(request):
    datas = [convertDate(request.POST['inicio']), convertDate(request.POST['fim'])]
    congregacoes = request.POST.getlist('congregacao')
    categorias = request.POST.getlist('categoria_entrada')
    formas = request.POST.getlist('forma')
    membros = request.POST.getlist('membro')

    entradas = Entrada.objects.filter(data__range = datas).order_by('data')
    entradas = entradas.filter(congregacao__nome__in = congregacoes) if congregacoes != [] else entradas
    entradas = entradas.filter(categoria__nome__in = categorias) if categorias != [] else entradas
    entradas = entradas.filter(transacao__nome__in = formas) if formas != [] else entradas
    entradas = entradas.filter(membro__nome__in = membros) if membros != [] else entradas

    if categorias == []:
        avulsas = EntradaAvulsa.objects.filter(data__range = datas).order_by('data')
        avulsas = avulsas.filter(congregacao__nome__in = congregacoes) if congregacoes != [] else avulsas

        return list(chain(entradas, avulsas))

    return entradas

def listaMissao(request):
    datas = [convertDate(request.POST['inicio']), convertDate(request.POST['fim'])]
    congregacoes = request.POST.getlist('congregacao')
    missoes = request.POST.getlist('missao')

    entradas = EntradaMissao.objects.filter(data__range = datas).order_by('data')
    entradas = entradas if congregacoes == [] else entradas.filter(missao__congregacao__nome__in = congregacoes)
    entradas = entradas if missoes == [] else entradas.filter(missao__nome__in = missoes)

    return entradas

def listaSaida(request):
    datas = [convertDate(request.POST['inicio']), convertDate(request.POST['fim'])]
    congregacoes = request.POST.getlist('congregacao')
    categorias = request.POST.getlist('categoria_saida')
    pagamentos = request.POST.getlist('transacao')
    empresas = request.POST.getlist('fornecedor')

    saidas = Saida.objects.filter(data__range = datas).order_by('data')
    saidas = saidas.filter(congregacao__nome__in = congregacoes) if congregacoes != [] else saidas
    saidas = saidas.filter(categoria__nome__in = categorias) if categorias != [] else saidas
    saidas = saidas.filter(transacao__nome__in = pagamentos) if pagamentos != [] else saidas
    saidas = saidas.filter(fornecedor__nome__in = empresas) if empresas != [] else saidas

    return saidas