from django.shortcuts import render

from .models import *
from .forms import *

import pandas as pd
from decimal import Decimal
import os
from datetime import datetime
from reportlab.pdfgen import canvas
from django.conf import settings
from pathlib import Path
from itertools import chain                     # Juntar duas listas de queryset de classes diferentes
from reportlab.platypus import Table

#pegando datas dos relatorios
dates = []

# Métodos Renderizados
def avulso(request, acao):
    if request.method == 'POST':
        formulario = EntradaAvulsaForm(request.POST)

        if formulario.is_valid():
            entrada = EntradaAvulsa()
            entrada.congregacao = Congregacao.objects.get(id = request.POST['congregacao'])
            entrada.data = convertDate(request.POST['data'])

            if 'descricao' in request.POST:
                entrada.descricao = request.POST['descricao']

            entrada.valor = request.POST['valor']

            if 'comprovante' in request.FILES:
                entrada.comprovante = request.FILES['comprovante']

            entrada.administrador = Administrador.objects.get(id = 1)

            entrada.save()

    return render(request, 'financeiro/paginas/avulso/adicionar.html', {'formulario' : EntradaAvulsaForm()})

def cadMembrosExcel(request):
    #Instalar o pandas
    #pip install pandas
    if request.method == 'POST':
        excel = Excel()
        form = FormExcel(request.POST, request.FILES)
        if form.is_valid():
            excel.arquivo = request.FILES['arquivo']
            excel.save() 
            dados = pd.read_excel(excel.arquivo.path)
            membros = []
            membros = dados
            for m in range(0, membros.__len__()):
                membrosExistente = Membro.objects.filter(CPF=membros['CPF'][m])
                if membrosExistente.__len__() == 1:
                    print("Já existe")
                else:
                    membro = Membro()
                    membro.CPF = membros['CPF'][m]
                    membro.nome = membros['NOME'][m]
                    membro.telefone = membros['TELEFONE'][m]
                    membro.profissao = membros['PROFISSAO'][m]
                    membro.save()
            excel.delete()
            return render(request, 'index.html', {})
    else:
        form = FormExcel()
    return render(request, 'financeiro/form_excel.html', {'form': form})

def categoria(request, acao):
    pagina = 0

    if request.method == 'POST':
        formulario = CategoriaSaidaForm(request.POST)

        if formulario.is_valid():
            categoria = CategoriaSaida()
            categoria.nome = request.POST['nome']
            
            if 'descricao' in request.POST:
                categoria.descricao = request.POST['descricao']
            
            categoria.save()

            pagina = 1
            
        return render(request, 'financeiro/paginas/categoria/adicionar.html', {'formulario' : CategoriaSaidaForm(), 'pagina' : pagina, 'id' : categoria.id, 'nome' : categoria.nome})

    return render(request, 'financeiro/paginas/categoria/adicionar.html', {'formulario' : CategoriaSaidaForm(), 'pagina' : pagina})

def catEntrada(request, acao):
    pagina = 0

    if request.method == 'POST':
        formulario = CategoriaEntradaForm(request.POST)

        if formulario.is_valid():
            categoria = CategoriaEntrada()
            categoria.nome = request.POST['nome']
            
            if 'descricao' in request.POST:
                categoria.descricao = request.POST['descricao']
            
            categoria.save()

            pagina = 1
            
        return render(request, 'financeiro/paginas/catentrada/adicionar.html', {'formulario' : CategoriaEntradaForm(), 'pagina' : pagina, 'id' : categoria.id, 'nome' : categoria.nome})

    return render(request, 'financeiro/paginas/catentrada/adicionar.html', {'formulario' : CategoriaEntradaForm(), 'pagina' : pagina})

def congregacao(request, acao):
    pagina = 0

    congregacao = Congregacao()

    if request.method == 'POST':
        formulario = CongregacaoForm(request.POST)

        if formulario.is_valid():
            congregacao.nome = request.POST['nome']
            congregacao.localidade = request.POST['localidade']
            congregacao.save()

            pagina = 1

            return render(request, 'financeiro/paginas/congregacao/adicionar.html', {'formulario' : CongregacaoForm(), 'pagina' : pagina, 'id' : congregacao.id, 'nome' : request.POST['nome']})

    return render(request, 'financeiro/paginas/congregacao/adicionar.html', {'formulario' : CongregacaoForm(), 'pagina' : pagina})

def empresa(request, acao):
    pagina = 0

    if request.method == 'POST':
        formulario = EmpresaForm(request.POST)

        if formulario.is_valid():
            empresa = Empresa()
            empresa.CPF_CNPJ = request.POST['CPF_CNPJ']
            empresa.nome = request.POST['nome']
            
            if 'descricao' in request.POST:
                empresa.descricao = request.POST['descricao']
            
            if 'endereco' in request.POST:
                empresa.endereco = request.POST['endereco']

            if 'cidade' in request.POST:
                empresa.cidade = request.POST['cidade']

            empresa.save()

            pagina = 1
            
        return render(request, 'financeiro/paginas/empresa/adicionar.html', {'formulario' : EmpresaForm(), 'pagina' : pagina, 'id' : empresa.id, 'nome' : empresa.nome})

    return render(request, 'financeiro/paginas/empresa/adicionar.html', {'formulario' : EmpresaForm(), 'pagina' : pagina})

def entrada(request, acao):
    if request.method == 'POST':
        formulario = EntradaForm(request.POST)

        if formulario.is_valid():
            entrada = Entrada()
            entrada.congregacao = Congregacao.objects.get(id = request.POST['congregacao'])
            entrada.categoria = CategoriaEntrada.objects.get(id = request.POST['categoria'])
            entrada.forma_de_Entrada = Pagamento.objects.get(id = request.POST['pagamento'])
            entrada.membro = Membro.objects.get(id = request.POST['membro'])

            if 'descricao' in request.POST:
                entrada.descricao = request.POST['descricao']

            entrada.valor = request.POST['valor']
            entrada.data = convertDate(request.POST['data'])

            if 'comprovante' in request.FILES:
                entrada.comprovante = request.FILES['comprovante']

            entrada.administrador = Administrador.objects.get(id = 1)

            entrada.save()

    return render(request, 'financeiro/paginas/entrada/adicionar.html', {'formulario' : EntradaForm()})

def index(request):
    return render(request, 'financeiro/index.html')

def membro(request, acao):
    pagina = 0

    if request.method == 'POST':
        formulario = MembroForm(request.POST)

        if formulario.is_valid():
            membro = Membro()
            membro.CPF = request.POST['CPF']
            membro.nome = request.POST['nome']
            
            if 'telefone' in request.POST:
                membro.telefone = request.POST['telefone']
            
            if 'profissao' in request.POST:
                membro.profissao = request.POST['profissao']

            membro.save()

            pagina = 1
            
        return render(request, 'financeiro/paginas/membro/adicionar.html', {'formulario' : MembroForm(), 'pagina' : pagina, 'id' : membro.id, 'nome' : membro.nome})

    return render(request, 'financeiro/paginas/membro/adicionar.html', {'formulario' : MembroForm(), 'pagina' : pagina})

def pagamento(request, acao):
    pagina = 0

    if request.method == 'POST':
        formulario = PagamentoForm(request.POST)

        if formulario.is_valid():
            pagamento = Pagamento()
            pagamento.nome = request.POST['nome']
            pagamento.save()

            pagina = 1
            
        return render(request, 'financeiro/paginas/pagamento/adicionar.html', {'formulario' : PagamentoForm(), 'pagina' : pagina, 'id' : pagamento.id, 'nome' : pagamento.nome})

    return render(request, 'financeiro/paginas/pagamento/adicionar.html', {'formulario' : PagamentoForm(), 'pagina' : pagina})

def saida(request, acao):
    if(request.method == 'POST'):
        formulario = SaidaForm(request.POST, request.FILES)

        if formulario.is_valid():
            saida = Saida()
            saida.congregacao = Congregacao.objects.get(id = request.POST['congregacao'])
            saida.categoria = CategoriaSaida.objects.get(id = request.POST['categoria'])
            saida.forma_de_Pagamento = Pagamento.objects.get(id = request.POST['pagamento'])
            saida.empresa = Empresa.objects.get(id = request.POST['empresa'])
            saida.nome = request.POST['nome']
            saida.descricao = request.POST['descricao']
            saida.valor = request.POST['valor']
            saida.data = convertDate(request.POST['data'])

            if('comprovante' in request.FILES):
                saida.comprovante = request.FILES['comprovante']

            if('nota_fiscal' in request.FILES):
                saida.nota_Fiscal = request.FILES['nota_fiscal']
            
            saida.administrador = Administrador.objects.get(id = 1)
            saida.save()
            
    return render(request, 'financeiro/paginas/saida/adicionar.html', {'formulario' : SaidaForm()})

# Métodos Auxiliares
def cabecalhoRelatorio(pdf, data):              # Insere Cabeçalhos Relatórios
    pdf.drawImage('ibc_financeiro/static/imagens/logo.png', 10,758,height=50, width=60)
    pdf.setFont('Times-Bold', 12)
    pdf.drawString(200,800,"IGREJA BATISTA DE CORRENTE")
    pdf.drawString(182,785,"Departamento de Administração e Finanças")
    pdf.drawString(240,770,"Relatório Financeiro")
    pdf.drawString(430,740,"Data: " + data)

def convertDate(date):                          # Converte formato da data
    return datetime.strptime(date, '%d/%m/%Y').date()

def gerarRelatorio(request, dados, tipo):
    data = str(date.today().strftime('%d/%m/%Y'))
    valorTotal = 0
    y = 0
    
    if tipo == 'saída':
        caminho = "ibc_financeiro/static/relatorio_saida.pdf"
        pdf = canvas.Canvas(caminho)
        pdf.setTitle("Relatório de Saidas")
        pdf.drawImage('ibc_financeiro/static/imagens/logo.png', 10,758,height=50, width=60)
        cabecalhoRelatorio(pdf, data)
        pdf.drawString(20, 700, "Data ")
        pdf.drawString(100, 700, "Congregação ")
        pdf.drawString(330,700,"Categoria ")
        pdf.drawString(490,700,"Valor ")
        pdf.drawString(278,755,"Saídas")
        pdf.line(275, 752, 315, 752)
        pdf.setFont('Helvetica', 10)
        #Listando todas as saidas
        for saida in dados:
            y = y + 30
            if(y > 580):
                y = 0
                pdf.showPage()
            pdf.setFont('Helvetica', 10)
            pdf.line(585, 718 - y, 10, 718 - y)
            pdf.drawString(20, 700 - y, str(saida.data.strftime('%d/%m/%Y')))
            pdf.drawString(100, 700 - y, str(saida.congregacao))
            pdf.drawString(330,700 - y, str(saida.categoria)[0:25])
            pdf.drawString(490,700 - y, str(saida.valor))
        
            valorTotal = valorTotal + saida.valor
        pdf.line(585, 690 - y, 10, 690 - y)
        pdf.setFont('Times-Bold', 12)
        pdf.drawString(400,650 - y,"Valor Total: "+" R$ "+str(valorTotal))
        pdf.showPage()
        #Adicionando os comprovantes
        for saida in dados:
            if str(saida.comprovante) != "":
                if saida.descricao != None:    
                    pdf.drawString(20, 780, str(saida.descricao))
                arquivo = "ibc_financeiro/"+str(saida.comprovante)
                pdf.drawImage(arquivo, 200, 250, width= 200, height= 400)
                pdf.showPage()
        pdf.save()
    elif tipo == 'entrada':
        caminho = "ibc_financeiro/static/relatorio_entrada.pdf"
        pdf = canvas.Canvas(caminho)
        pdf.setTitle("Relatório de Entradas")
        cabecalhoRelatorio(pdf, data)
        pdf.drawString(20, 700, "Data ")
        pdf.drawString(100, 700, "Congregação ")
        pdf.drawString(330,700,"Categoria ")
        pdf.drawString(490,700,"Valor ")
        pdf.drawString(278,755,"Entradas")
        pdf.line(275, 752, 330, 752)
        pdf.setFont('Helvetica', 10)
        for entrada in dados:
            y = y + 30
            if(y > 580):
                y = 0
                pdf.showPage()
            pdf.setFont('Helvetica', 10)
            pdf.line(585, 718 - y, 10, 718 - y)
            pdf.drawString(20, 700 - y, str(entrada.data.strftime('%d/%m/%Y')))
            pdf.drawString(100, 700 - y, str(entrada.congregacao))
            if hasattr(entrada, 'categoria'):
                pdf.drawString(330,700 - y, str(entrada.categoria)[0:25])
            else:
                pdf.drawString(330,700 - y, "Avulsa")
            pdf.drawString(490,700 - y, str(entrada.valor))
        
            valorTotal = valorTotal + entrada.valor
        pdf.line(585, 690 - y, 10, 690 - y)
        pdf.setFont('Times-Bold', 12)
        pdf.drawString(400,650 - y,"Valor Total: "+" R$ "+str(valorTotal))

        pdf.showPage()
        for entrada in dados:
            if str(entrada.comprovante) != "":
                if entrada.descricao != None:    
                    pdf.drawString(20, 780, str(entrada.descricao))
                arquivo = "ibc_financeiro/"+str(entrada.comprovante)
                pdf.drawImage(arquivo, 200, 250, width= 200, height= 400)
                pdf.showPage()
        pdf.save()
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
        pdf.drawImage('ibc_financeiro/static/imagens/logo.png', 10,758,height=50, width=60)
        cabecalhoRelatorio(pdf, data)
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
                progressoMissao(pdf, meta, valorTotal, 670 - y)
            else:
                progressoMissao(pdf, meta, valorTotal, 600 - y)
            valorTotal = 0
            meta = 0
            y += 150
        pdf.save()
    
def gerarRelatorioGeral(request, entradas, saidas, missoes):
    data = str(date.today().strftime('%d/%m/%Y'))
    
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
    pdf.drawString(50, 700 - y, 'Ofertas Avulsas:......................................: ')
    pdf.drawString(365, 700 - y , " R$  "+str(valorEntradasAvulsa))
    pdf.line(363, 698 - y, 550, 698 - y)
    pdf.drawString(50, 678 - y , 'Missões:......................................: ') 
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
            if entrada.categoria.nome == 'Dizimo':
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
    pdf.showPage()
    #Adicionando os comprovantes
    for saida in saidas:
        if saida.comprovante != "":
            pdf.drawString(20, 780, str(saida.nome))
            arquivo = "ibc_financeiro/"+str(saida.comprovante)
            pdf.drawImage(arquivo, 150, 250, width= 250, height= 400)
            pdf.showPage()
    pdf.save()

def relatorio(request, tipo):
    if tipo == 'entrada':
        if request.method == 'POST':
            gerarRelatorio(request, listaEntrada(request), tipo)
            return render(request, 'index.html', {'nome': 'relatorio_entrada.pdf'})

        return render(request, 'financeiro/paginas/relatorio.html', {'title' : tipo, 'formulario' : RelatorioEntradaForm()})

    elif tipo == 'saída':
        if request.method == 'POST':
            gerarRelatorio(request, listaSaida(request), tipo)

            return render(request, 'index.html', {'nome': 'relatorio_saida.pdf'})

        return render(request, 'financeiro/paginas/relatorio.html', {'title' : tipo, 'formulario' : RelatorioSaidaForm()})

    elif tipo == 'missão':
        if request.method == 'POST':
            gerarRelatorio(request, listaMissao(request), tipo)
            return render(request, 'index.html', {'nome': 'relatorio_missões.pdf'})
        return render(request, 'financeiro/paginas/relatorio.html', {'title' : tipo, 'formulario' : RelatorioMissaoForm()})

    elif tipo == 'geral':
        if request.method == 'POST':
            gerarRelatorioGeral(request, listaEntrada(request), listaSaida(request), listaMissao(request))
            return render(request, 'index.html', {'nome': 'relatorio_geral.pdf'})
        return render(request, 'financeiro/paginas/relatorio.html', {'title' : tipo, 'formulario' : RelatorioGeralForm()})

def listaEntrada(request):
    datas = [convertDate(request.POST['inicio']), convertDate(request.POST['fim'])]
    dates.append([convertDate(request.POST['inicio']), convertDate(request.POST['fim'])])
    congregacoes = request.POST.getlist('congregacao')
    categorias = request.POST.getlist('categoria_entrada')
    formas = request.POST.getlist('forma')
    membros = request.POST.getlist('membro')

    entradas = Entrada.objects.filter(data__range = datas).order_by('data')
    entradas = entradas.filter(congregacao__nome__in = congregacoes) if congregacoes != [] else entradas
    entradas = entradas.filter(categoria__nome__in = categorias) if categorias != [] else entradas
    entradas = entradas.filter(forma_de_Entrada__nome__in = formas) if formas != [] else entradas
    entradas = entradas.filter(membro__nome__in = membros) if membros != [] else entradas

    avulsas = EntradaAvulsa.objects.filter(data__range = datas).order_by('data')
    avulsas = avulsas.filter(congregacao__nome__in = congregacoes) if congregacoes != [] else avulsas

    return list(chain(entradas, avulsas))

def listaGeral(request):
    entradas = listaEntrada(request)
    saidas = listaSaida(request)

    return list(chain(entradas, saidas))

def listaMissao(request):
    datas = [convertDate(request.POST['inicio']), convertDate(request.POST['fim'])]
    congregacoes = request.POST.getlist('congregacao')
    missoes = request.POST.getlist('missao')
    andamento = True if 'andamento' in request.POST else False

    print(andamento)

    entradas = EntradaMissao.objects.filter(data__range = datas).order_by('data')
    entradas = entradas if congregacoes == [] else entradas.filter(missao__congregacao__nome__in = congregacoes)
    entradas = entradas if missoes == [] else entradas.filter(missao__nome__in = missoes)
    entradas = entradas if andamento == False else entradas.filter(missao__em_Andamento = andamento)

    return entradas

def listaSaida(request):
    datas = [convertDate(request.POST['inicio']), convertDate(request.POST['fim'])]
    congregacoes = request.POST.getlist('congregacao')
    categorias = request.POST.getlist('categoria_saida')
    pagamentos = request.POST.getlist('pagamento')
    empresas = request.POST.getlist('empresa')

    saidas = Saida.objects.filter(data__range = datas).order_by('data')
    saidas = saidas.filter(congregacao__nome__in = congregacoes) if congregacoes != [] else saidas
    saidas = saidas.filter(categoria__nome__in = categorias) if categorias != [] else saidas
    saidas = saidas.filter(forma_de_Pagamento__nome__in = pagamentos) if pagamentos != [] else saidas
    saidas = saidas.filter(empresa__nome__in = empresas) if empresas != [] else saidas

    return saidas

def progressoMissao(pdf, meta, total, y):
    pdf.drawString(100, y, 'Meta: R$ ' + '{:.2f}'.format(meta))

    pdf.line(100, y - 5, 500, y - 5)

    pdf.line(100, y - 5, 100, y - 25)

    porcentagem = int((total * 100) / meta)
    final = int((400 * porcentagem) / 100)

    
    pdf.setStrokeColorRGB(0,1,0.3)

    comeco = 101

    for x in range(101, final + 99):
        pdf.line(x, y - 5.5, x, y - 24.5)
        pdf.line(x + 0.5, y - 5.5, x, y - 24.5)
        comeco = x

    pdf.setStrokeColorRGB(1, 0, 0)   

    for x in range(comeco + 1, 500):
        pdf.line(x, y - 5.5, x, y - 24.5)
        pdf.line(x + 0.5, y - 5.5, x, y - 24.5)
        
    pdf.setStrokeColorRGB(0,0,0)
    
    pdf.line(500, y - 5, 500, y - 25) 
    pdf.line(100, y - 25, 500, y - 25)

    pdf.drawString(100, y - 38, 'Alcançado: R$ ' + '{:.2f}'.format(total))
    pdf.drawString(383, y - 38, 'Restante: R$ ' + '{:.2f}'.format(meta - total))