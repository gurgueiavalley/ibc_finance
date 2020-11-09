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

def index(request):
    return render(request, 'financeiro/index.html')

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
            listaMissao(request)

        return render(request, 'financeiro/paginas/relatorio.html', {'title' : tipo, 'formulario' : RelatorioMissaoForm()})

    elif tipo == 'geral':
        if request.method == 'POST':
            listaGeral(request)
        
        return render(request, 'financeiro/paginas/relatorio.html', {'title' : tipo, 'formulario' : RelatorioGeralForm()})

# Métodos Auxiliares
def cabecalhoRelatorio(pdf, data, y):           # Insere o cabeçalho dos relatórios
    pdf.drawImage('ibc_financeiro/static/imagens/logo.png', 10,758,height=50, width=60)
    pdf.setFont('Times-Bold', 12)
    pdf.drawString(200,800,"IGREJA BATISTA DE CORRENTE")
    pdf.drawString(182,785,"Departamento de Administração e Finanças")
    pdf.drawString(240,770,"Relatório Financeiro")
    pdf.drawString(430,740,"Data: " + data)
    pdf.drawString(20, 700 - y, "Data ")
    pdf.drawString(100, 700 - y, "Congregação ")
    pdf.drawString(330,700 - y,"Categoria ")
    pdf.drawString(490,700 - y,"Valor ")

def convertDate(date):                          # Converte formato da data
    return datetime.strptime(date, '%d/%m/%Y').date()

def gerarRelatorio(request, dados, tipo):
    data = str(date.today())
    valorTotal = 0
    y = 0
    
    if tipo == 'saída':
        caminho = "ibc_financeiro/static/relatorio_saida.pdf"
        pdf = canvas.Canvas(caminho)
        pdf.setTitle("Relatório de Saidas")
        pdf.drawImage('ibc_financeiro/static/imagens/logo.png', 10,758,height=50, width=60)
        cabecalhoRelatorio(pdf, data, y)
        pdf.drawString(278,755,"Saídas")
        pdf.line(275, 752 - y, 315, 752 - y)
        pdf.setFont('Helvetica', 10)
        #Listando todas as saidas
        for saida in dados:
            y = y + 30
            if(y > 800):
                y = 0
                pdf.showPage()
            pdf.line(585, 718 - y, 10, 718 - y)
            pdf.drawString(20, 700 - y, str(saida.data))
            pdf.drawString(100, 700 - y, str(saida.congregacao))
            pdf.drawString(330,700 - y, str(saida.categoria))
            pdf.drawString(490,700 - y, str(saida.valor))
        
            valorTotal = valorTotal + saida.valor
        pdf.line(585, 690 - y, 10, 690 - y)
        pdf.setFont('Times-Bold', 12)
        pdf.drawString(400,650 - y,"Valor Total: "+" R$ "+str(valorTotal))
        pdf.showPage()
        #Adicionando os comprovantes
        for saida in dados:
            if str(saida.comprovante) != "":
                arquivo = "ibc_financeiro/"+str(saida.comprovante)
                pdf.drawImage(arquivo, 150, 250, width= 250, height= 400)
                pdf.showPage()
        pdf.save()
    elif tipo == 'entrada':
        caminho = "ibc_financeiro/static/relatorio_entrada.pdf"
        pdf = canvas.Canvas(caminho)
        pdf.setTitle("Relatório de Entradas")
        cabecalhoRelatorio(pdf, data, y)
        pdf.drawString(278,755,"Entradas")
        pdf.line(275, 752 - y, 330, 752 - y)
        pdf.setFont('Helvetica', 10)
        for entrada in dados:
            y = y + 30
            if(y > 800):
                y = 0
                pdf.showPage()
            pdf.line(585, 718 - y, 10, 718 - y)
            pdf.drawString(20, 700 - y, str(entrada.data))
            pdf.drawString(100, 700 - y, str(entrada.congregacao))
            pdf.drawString(330,700 - y, str(entrada.categoria))
            pdf.drawString(490,700 - y, str(entrada.valor))
        
            valorTotal = valorTotal + entrada.valor
        pdf.line(585, 690 - y, 10, 690 - y)
        pdf.setFont('Times-Bold', 12)
        pdf.drawString(400,650 - y,"Valor Total: "+" R$ "+str(valorTotal))

        pdf.showPage()
        for entrada in dados:
            if str(entrada.comprovante) != "":
                arquivo = "ibc_financeiro/"+str(entrada.comprovante)
                pdf.drawImage(arquivo, 150, 250, width= 250, height= 400)
                pdf.showPage()
        pdf.save()

def listaEntrada(request):
    datas = [convertDate(request.POST['inicio']), convertDate(request.POST['fim'])]
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