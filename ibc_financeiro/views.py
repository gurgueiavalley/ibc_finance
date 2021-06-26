from django.shortcuts import redirect, render

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
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

from .functions.report import *
from .functions.file    import *

from django.db.models import Sum
from django.urls import reverse
from django.contrib import messages

#pegando datas dos relatorios
dates = []


# Métodos Renderizados
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
    pagina = 0

    if request.method == 'POST':
        formulario = CategoriaForm(request.POST)

        if formulario.is_valid():
            categoria = Categoria()
            categoria.nome = request.POST['nome']
            categoria.tipo = 'SAÍDA'
            
            categoria.save()

            pagina = 1
            
        return render(request, 'financeiro/paginas/categoria/adicionar.html', {'formulario' : CategoriaForm(), 'pagina' : pagina, 'id' : categoria.id, 'nome' : categoria.nome})

    return render(request, 'financeiro/paginas/categoria/adicionar.html', {'formulario' : CategoriaForm(), 'pagina' : pagina})



@login_required(login_url='/conta/login')
def catEntrada(request, acao):
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

    return render(request, 'financeiro/paginas/catentrada/adicionar.html', {'formulario' : CategoriaForm(), 'pagina' : pagina})



@login_required(login_url='/conta/login')
def congregacao(request, acao):
    pagina = 0

    congregacao = Congregacao()

    if request.method == 'POST':
        formulario = CongregacaoForm(request.POST)

        if formulario.is_valid():
            congregacao.nome = request.POST['nome']
            congregacao.save()

            pagina = 1

            return render(request, 'financeiro/paginas/congregacao/adicionar.html', {'formulario' : CongregacaoForm(), 'pagina' : pagina, 'id' : congregacao.id, 'nome' : request.POST['nome']})

    return render(request, 'financeiro/paginas/congregacao/adicionar.html', {'formulario' : CongregacaoForm(), 'pagina' : pagina})



@login_required(login_url='/conta/login')
def emissao(request, acao):
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
            
            return render(request, 'financeiro/paginas/empresa/adicionar.html', {'formulario' : FornecedorForm(), 'pagina' : pagina, 'id' : fornecedor.id, 'nome' : fornecedor.nome})

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
            membro.delete()
            messages.success(request, "DELETADO COM SUCESSO!")
            return redirect('/listar/membros')
        else:
            entradas = Entrada.objects.filter(membro_id=membro.id)
            return render(request, 'financeiro/paginas/membro/deletar.html', {'membro': membro,'entradas': entradas})
    
    elif acao == 'alterar':
        membro = Membro.objects.get(id = request.GET.get('id'))

        if request.method == 'POST':
            formulario = MembroForm(request.POST)
            if formulario.is_valid():
                membro.CPF = request.POST['CPF']
                membro.nome = request.POST['nome']
                membro.celular = request.POST['celular']
                membro.email = request.POST['email']
                membro.sexo = request.POST['sexo']
                membro.nascimento = convertDate(request.POST['nascimento'])

                membro.save()
            messages.success(request, "ALTERADO COM SUCESSO!")
            return redirect('/listar/membros')
        
        else:
            return render(request, 'financeiro/paginas/membro/alterar.html', {'formulario': MembroForm(), 'membro': membro})
    
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
        usuarios = User.objects.all()
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
        usuario = User.objects.get(id = request.user.id)
        
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

            pagina = 1

            return render(request, 'financeiro/paginas/missao/adicionar.html', {'formulario' : MissaoForm(), 'pagina' : pagina, 'id' : missao.id, 'nome' : request.POST['nome']})

    if acao == 'listar':
        tipo = 'missao'
        return render(request, 'financeiro/paginas/form_listar.html', {'title': tipo,'formulario' : RelatorioMissaoForm()})

    return render(request, 'financeiro/paginas/missao/adicionar.html', {'formulario' : MissaoForm(), 'pagina' : pagina})



@login_required(login_url='/conta/login')
def pagamento(request, acao):
    pagina = 0

    if request.method == 'POST':
        formulario = TransacaoForm(request.POST)

        if formulario.is_valid():
            transacao = Transacao()
            transacao.nome = request.POST['nome']
            transacao.save()

            pagina = 1
            
        return render(request, 'financeiro/paginas/pagamento/adicionar.html', {'formulario' : TransacaoForm(), 'pagina' : pagina, 'id' : transacao.id, 'nome' : transacao.nome})

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



def conta(request, acao):
    if acao == 'login':
        if request.method == 'POST':
            user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('index')
            else:
                alert = 'USUARIO OU SENHA INCORRETOS!'
                return render(request, 'financeiro/paginas/conta/login.html', {'alert': alert})  
        return render(request, 'financeiro/paginas/conta/login.html')
    if acao == 'logout':
        logout(request)
        return render(request, 'financeiro/paginas/conta/login.html')
    if acao == 'recuperar':
        if request.method == 'POST':
            return  HttpResponse ('<div style="text-align: center; padding-top: 20%;"><h3>Em desenvolvimento, por favor aguarde! </h3></div>')
        return render(request, 'financeiro/paginas/conta/recuperar.html')



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

    elif tipo == 'missao':
        missoes = listaMissao(request)
        return render(request, 'financeiro/paginas/missao/tabela.html', {'missoes' : missoes})

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
    pdf.drawImage('ibc_financeiro/static/imagens/logo.jpg', 10, 758, height = 60, width = 60)

    pdf.setFont('Times-Bold', 12)
    
    pdf.drawString(200, 800, 'IGREJA BATISTA DE CORRENTE')
    pdf.drawString(182, 785, 'Departamento de Administração e Finanças')
    pdf.drawString(240, 770, 'Relatório Financeiro')
    
    pdf.drawString(430, 740, 'Data: ' + data)

def convertDate(date):                          # Converte formato da data
    return datetime.strptime(date, '%d/%m/%Y').date()

def getData():
    return date.today().strftime('%d/%m/%Y')

def gerarRelatorio(request, dados, tipo):
    total, y = 0, 0
    
    if tipo == 'entrada':
        directory = 'ibc_financeiro/static/entrada.pdf'

        pdf = canvas.Canvas(directory)
        pdf.setTitle('Relatório de Entradas')

        cabecalhoRelatorio(pdf, str(getData()))

        pdf.drawString(278, 755, 'Entradas')
        pdf.line(275, 752, 330, 752)

        pdf.drawString(20, 700, 'Data')
        pdf.drawString(100, 700, 'Congregação')
        pdf.drawString(330, 700, 'Categoria')
        pdf.drawString(490, 700, 'Valor')

        pdf.setFont('Helvetica', 10)

        for entrada in dados:
            y = y + 30

            if(y > 580):
                y = 0

                pdf.showPage()

            pdf.line(585, 718 - y, 10, 718 - y)

            pdf.drawString(20, 700 - y, str(entrada.data.strftime('%d/%m/%Y')))
            pdf.drawString(100, 700 - y, str(entrada.congregacao)[0:35])

            if hasattr(entrada, 'categoria'):
                pdf.drawString(330, 700 - y, str(entrada.categoria)[0:25])

            else:
                pdf.drawString(330, 700 - y, 'AVULSA')

            pdf.drawString(490, 700 - y, 'R$ ' + str(entrada.valor))
        
            total += entrada.valor
        
        pdf.line(585, 690 - y, 10, 690 - y)

        pdf.setFont('Times-Bold', 12)

        pdf.drawString(400, 650 - y, 'Valor Total: R$ ' + str(total))

        pdf.save()

        Report.receipt(dados, directory, 'ibc_financeiro/static/pdf/report/entry.pdf')

    if tipo == 'saida':
        directory = 'ibc_financeiro/static/saida.pdf'
        
        pdf = canvas.Canvas(directory)
        pdf.setTitle('Relatório de Saidas')
        
        cabecalhoRelatorio(pdf, str(getData()))
        pdf.drawString(278, 755, 'Saídas')
        pdf.line(275, 752, 315, 752)

        pdf.drawString(20, 700, 'Data ')
        pdf.drawString(100, 700, 'Congregação ')
        pdf.drawString(330, 700, 'Categoria ')
        pdf.drawString(490, 700, 'Valor ')
        
        pdf.setFont('Helvetica', 10)

        for saida in dados:
            y = y + 30

            if(y > 580):
                y = 0

                pdf.showPage()
            
            pdf.line(585, 718 - y, 10, 718 - y)

            pdf.drawString(20, 700 - y, str(saida.data.strftime('%d/%m/%Y')))
            pdf.drawString(100, 700 - y, str(saida.congregacao)[0:35])
            pdf.drawString(330, 700 - y, str(saida.categoria)[0:25])
            pdf.drawString(490, 700 - y, 'R$ ' + str(saida.valor))
        
            total += + saida.valor
        
        pdf.line(585, 690 - y, 10, 690 - y)

        pdf.setFont('Times-Bold', 12)

        pdf.drawString(400, 650 - y, 'Valor Total: ' + 'R$ ' + str(total))
        
        pdf.save()

        Report.receipt(dados, directory, 'ibc_financeiro/static/pdf/report/exit.pdf')
    
    if tipo == 'missão':
        valorTotal = 0
        meta = 0
        y = 0
        pagina = False
        nomes_missoes = []
        for missoes in dados:
            if missoes.missao.nome not in nomes_missoes:
                nomes_missoes.append(missoes.missao.nome)

        caminho = "ibc_financeiro/static/relatorio_missões.pdf"
        pdf = canvas.Canvas(caminho)
        pdf.setTitle("Relatório de Missões")
        pdf.drawImage('ibc_financeiro/static/imagens/logo.jpg', 10,758,height=50, width=60)
        cabecalhoRelatorio(pdf, str(getData()))
        pdf.drawString(275,755,"Missões")
        pdf.line(272, 752, 317, 752)
        
        for item in nomes_missoes:
            if pagina == False and y > 450:
                y = 0
                pdf.showPage()
                pagina = True
            if pagina:
                if y > 550:
                    y = 0
                    pdf.showPage()
                pdf.setFont('Times-Bold', 12)
                pdf.drawString(25, 750 - y, item)

                pdf.rect(100, 695 - y, 200, 30)
                pdf.drawString(105, 700 - y, "Data")
                pdf.rect(300, 695 - y, 200, 30)
                pdf.drawString(305, 700 - y, "Valor")
            else:    
                pdf.setFont('Times-Bold', 12)
                pdf.drawString(25, 685 - y, item)

                pdf.rect(100, 630 - y, 200, 30)
                pdf.drawString(105, 635 - y, "Data")
                pdf.rect(300, 630 - y, 200, 30)
                pdf.drawString(305, 635 - y, "Valor")
            for missoes in dados:
                if missoes.missao.nome == item:        
                    if pagina == False and y > 450:
                        y = 0
                        pdf.showPage()
                        pagina = True
                    if pagina:
                        if y > 550:
                            y = 0
                            pdf.showPage()
                        pdf.setFont('Helvetica', 10)
                        pdf.rect(100, 665 - y, 200, 30)
                        pdf.drawString(105, 670 - y, str(missoes.data.strftime('%d/%m/%Y')))
                        pdf.rect(300, 665 - y, 200, 30)
                        pdf.drawString(305, 670 - y, "R$  "+str(missoes.valor))
                        valorTotal += missoes.valor
                        meta = missoes.missao.meta
                        y += 30            
                    else:    
                        pdf.setFont('Helvetica', 10)
                        pdf.rect(100, 600 - y, 200, 30)
                        pdf.drawString(105, 605 - y, str(missoes.data.strftime('%d/%m/%Y')))
                        pdf.rect(300, 600 - y, 200, 30)
                        pdf.drawString(305, 605 - y, "R$  "+str(missoes.valor))
                        valorTotal += missoes.valor
                        meta = missoes.missao.meta
                        y += 30
            
            if pagina:
                Chart.progress(pdf, meta, valorTotal, 670 - y)
            
            else:
                Chart.progress(pdf, meta, valorTotal, 600 - y)

            valorTotal = 0
            meta = 0
            y += 150
        pdf.save()

def gerarRelatorioGeral(request, entradas, saidas, missoes):
    data = str(getData())
    
    valorEntradasAvulsa = 0
    valorMissao = 0
    valorTotalEntradas = 0
    valorTotalSaidas = 0
    
    categorias_entradas = []
    valor_entradas = 0

    #Pegando as categorias
    for entrada in entradas:
        if hasattr(entrada, 'categoria'):
            if entrada.categoria.nome not in categorias_entradas:
                categorias_entradas.append(entrada.categoria.nome)
        else:
            valorEntradasAvulsa += entrada.valor
    
    for missao in missoes:
        valorMissao += missao.valor
    valorTotalEntradas += valorEntradasAvulsa + valorMissao

    y = 0
    pagina = False
    
    caminho = "ibc_financeiro/static/relatorio_geral.pdf"
    pdf = canvas.Canvas(caminho)
    pdf.setTitle("Relatório Geral")
    cabecalhoRelatorio(pdf, data)
    pdf.drawString(260,755,"Recebimentos")
    pdf.line(257, 752, 335, 752)
    pdf.setFont('Helvetica', 10)

    #Adicionando categorias dinamicas
    for item in categorias_entradas:
        for entrada in entradas:
            if hasattr(entrada, 'categoria'):    
                if entrada.categoria.nome == item:
                    valor_entradas += entrada.valor
        valorTotalEntradas += valor_entradas
        pdf.drawString(50, 700 - y, item[0:30]+':......................................: ')
        pdf.drawString(365, 702 -y , " R$  "+str(valor_entradas))
        pdf.line(363, 700 - y, 550, 700 - y) 
        y += 20
        valor_entradas = 0                     
    pdf.drawString(50, 700 - y, 'OFERTAS AVULSAS:......................................: ')
    pdf.drawString(365, 700 - y , " R$  "+str(valorEntradasAvulsa))
    pdf.line(363, 698 - y, 550, 698 - y)
    pdf.drawString(50, 678 - y , 'MISSÕES:......................................: ') 
    pdf.drawString(365, 678 - y, " R$  "+str(valorMissao))
    pdf.line(363, 676 - y, 550, 676 - y)
    pdf.setFont('Times-Bold', 12)
    pdf.drawString(245, 642 - y, 'Total de Entradas: R$  ')
    pdf.drawString(365, 642 - y, str(valorTotalEntradas))
    pdf.line(363, 640 - y, 550, 640 - y)
    pdf.drawString(260, 600 - y, 'Pagamentos')
    pdf.line(257, 598 - y, 325, 598 - y)
    pdf.setFont('Helvetica', 10)
    
    #Adicionando Saidas
    for saida in range(1,len(saidas)+1): 
        y = y + 30
        valorTotalSaidas = valorTotalSaidas + saidas[saida - 1].valor

        if pagina == False and y > 450:
            y = 0
            pdf.showPage()
            pagina = True
        if pagina == True:
            if y > 600:
                y = 0
                pdf.showPage()    
            pdf.setFont('Helvetica', 10)       
            pdf.drawString(50, 750 - y, str(saida)+' º - '+str(saidas[saida - 1]))
            pdf.line(70, 748 - y, 343, 748 -y)
            pdf.drawString(345, 748 - y, ' R$')
            pdf.drawString(365, 750 - y, str(saidas[saida - 1].valor))
            pdf.line(363, 748 - y, 550, 748 - y)
        else:
            pdf.setFont('Helvetica', 10)       
            pdf.drawString(50, 580 - y, str(saida)+' º - '+str(saidas[saida - 1]))
            pdf.line(70, 578 - y, 343, 578 -y)
            pdf.drawString(345, 578 - y, ' R$')
            pdf.drawString(365, 580 - y, str(saidas[saida - 1].valor))
            pdf.line(363, 578 - y, 550, 578 - y)

    if pagina == True:
        if y > 600:
            y = 0
            pdf.showPage()
        pdf.setFont('Times-Bold', 12)
        pdf.drawString(265, 720 - y, 'Total de Saída: R$  ')
        pdf.drawString(365, 720 - y, str(valorTotalSaidas))
        pdf.line(363, 718 - y, 550, 718 - y)
        pdf.drawString(276, 698 - y, 'A Depositar: R$  ')
        pdf.line(363, 698 - y, 550, 698 - y)
    else:
        pdf.setFont('Times-Bold', 12)
        pdf.drawString(265, 555 - y, 'Total de Saída: R$  ')
        pdf.drawString(365, 557 - y, str(valorTotalSaidas))
        pdf.line(363, 555 - y, 550, 555 - y)
        pdf.drawString(276, 535 - y, 'A Depositar: R$  ')
        pdf.line(363, 535 - y, 550, 535 - y)
    pdf.drawString(20, 80, 'Conferido por: ')
    pdf.line(0, 60, 200, 60)
    pdf.line(210, 60, 400, 60)
    pdf.line(410, 60, 600, 60)
    pdf.showPage()

    #Adicionando Pagina de Dizimos 
    pdf.setFont('Times-Bold', 14)
    pdf.drawString(180, 750, 'IGREJA BATISTA DE CORRENTE')
    pdf.rect(20, 745, height=20, width=553)
    pdf.setFont('Helvetica', 10)
    pdf.drawString(230, 720, 'CONTROLE DE DÍZIMOS')
    pdf.drawString(219, 700, 'De: '+str(dates[0][0].strftime('%d/%m/%Y'))+' Até: '+str(dates[0][1].strftime('%d/%m/%Y')))

    pdf.setFont('Helvetica-Bold', 10)
    pdf.drawString(180, 650, 'RELAÇÃO NOMINAL')
    pdf.rect(20, 645, height=20, width=400)
    pdf.drawString(435, 650, 'VALOR')
    pdf.rect(420, 645, height=20, width=152)
    y = 0
    valorEntradas = 0
    for entrada in entradas:
        if hasattr(entrada, 'categoria'):
            if entrada.categoria.nome == 'DÍZIMO':
                if y > 500:
                    y = 0
                    pdf.showPage()
                y += 20
                valorEntradas += entrada.valor
                pdf.setFont('Helvetica', 10)
                pdf.drawString(35, 650 - y, str(entrada.membro.nome))
                pdf.rect(20, 645 - y, height=20, width=400)
                pdf.drawString(435, 650 - y, 'R$  '+str(entrada.valor))
                pdf.rect(420, 645 - y, height=20, width=152)
    y += 20
    pdf.setFont('Helvetica-Bold', 10)
    pdf.drawString(370, 650 - y, 'TOTAL')
    pdf.rect(20, 645 - y, height=20, width=400)
    pdf.drawString(435, 650 - y, 'R$  '+str(valorEntradas))
    pdf.rect(420, 645 - y, height=20, width=152)
    
    pdf.save()

    Report.receipt(saidas, caminho, 'ibc_financeiro/static/general.pdf')

    Chart.pie(saidas)

    directories = [
        'ibc_financeiro/static/general.pdf',
        'ibc_financeiro/static/chart.pdf'
    ]

    PDF.merge(directories, 'ibc_financeiro/static/pdf/report/general.pdf')
    File.delete(directories)

@login_required(login_url = '/conta/login')
def relatorio(request, tipo):
    if tipo == 'entrada':
        if request.method == 'POST':
            gerarRelatorio(request, listaEntrada(request), tipo)

            return render(request, 'index.html', {'nome': 'pdf/report/entry.pdf'})

        return render(request, 'financeiro/paginas/relatorio.html', {'title' : tipo, 'formulario' : RelatorioEntradaForm()})

    elif tipo == 'saida':
        if request.method == 'POST':
            gerarRelatorio(request, listaSaida(request), tipo)

            return render(request, 'index.html', {'nome': 'pdf/report/exit.pdf'})

        return render(request, 'financeiro/paginas/relatorio.html', {'title' : tipo, 'formulario' : RelatorioSaidaForm()})

    elif tipo == 'missão':
        if request.method == 'POST':
            gerarRelatorio(request, listaMissao(request), tipo)
            return render(request, 'index.html', {'nome': 'relatorio_missões.pdf'})
        return render(request, 'financeiro/paginas/relatorio.html', {'title' : tipo, 'formulario' : RelatorioMissaoForm()})

    elif tipo == 'geral':
        if request.method == 'POST':
            gerarRelatorioGeral(request, listaEntrada(request), listaSaida(request), listaMissao(request))
            
            return render(request, 'index.html', {'nome': 'pdf/report/general.pdf'})
        
        return render(request, 'financeiro/paginas/relatorio.html', {'title' : tipo, 'formulario' : RelatorioGeralForm()})

def listaEntrada(request):
    datas = [convertDate(request.POST['inicio']), convertDate(request.POST['fim'])]
    dates.append([convertDate(request.POST['inicio']), convertDate(request.POST['fim'])])
    congregacoes = request.POST.getlist('congregacao')
    categorias = request.POST.getlist('categoria_entrada')
    formas = request.POST.getlist('transacao')
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