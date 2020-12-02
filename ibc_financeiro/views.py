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
from itertools import chain

import webbrowser

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

def relatorio(request):
    if request.method == 'POST':
        print(request.POST)
        valor_Final_Entrada = 0
        valor_Final_Entrada_Avulsa = 0
        valor_Final_Entrada_Misssao = 0
        y = 0
        caminho = "ibc_financeiro/static/relatorio_entrada.pdf"
        pdf = canvas.Canvas(caminho)
        pdf.setTitle("Relatório de Entradas")
        pdf.drawImage('ibc_financeiro/static/imagens/logo.png', 10,780,height=50, width=60)
        pdf.setFont('Times-Bold', 24)
        pdf.drawString(200,800,"Relatório de Entradas")
        pdf.setFont('Times-Bold', 16)
        pdf.drawString(20, 750 - y, "Entradas")
        pdf.setFont('Helvetica', 12)
        for entrada in Entrada.objects.filter(congregacao__nome = request.POST['congregacao'],data__range=[request.POST['dataInicio'], request.POST['dataFim']]).order_by('data'):
            y = y + 30
            if(y > 800):
                y = 0
                pdf.showPage()
            pdf.drawString(40, 750 - y, "Data: " +  str(entrada.data))
            pdf.drawString(220,750 - y,"Categoria: " + str(entrada.categoria))
            pdf.drawString(420,750 - y,"Valor: " + str(entrada.valor))
            valor_Final_Entrada = valor_Final_Entrada + entrada.valor

        pdf.setFont('Times-Bold', 16)
        pdf.drawString(20, 720 - y, "Entradas Avulsa")
        pdf.setFont('Helvetica', 12)

        for entradaAvulsa in EntradaAvulsa.objects.filter(congregacao__nome = request.POST['congregacao'],data__range=[request.POST['dataInicio'], request.POST['dataFim']]).order_by('data'):
            y = y + 30
            if(y > 800):
                y = 0
                pdf.showPage()
            pdf.drawString(40, 720 - y, "Data: " +  str(entradaAvulsa.data))
            pdf.drawString(420,720 - y,"Valor: " + str(entradaAvulsa.valor))
            valor_Final_Entrada_Avulsa = valor_Final_Entrada_Avulsa + entradaAvulsa.valor
        

        pdf.setFont('Times-Bold', 16)
        pdf.drawString(20, 690 - y, "Entradas de Missões")
        pdf.setFont('Helvetica', 12)

        for missao in EntradaMissao.objects.filter(missao__congregacao__nome = request.POST['congregacao'],data__range=[request.POST['dataInicio'], request.POST['dataFim']]).order_by('data'):
            y = y + 30
            if(y > 600):
                y = 0
                pdf.showPage()
                y = 0
            pdf.drawString(40, 680 - y, "Data: " +  str(missao.data))
            pdf.drawString(200,680 - y,"Missão: " + str(missao.missao))
            pdf.drawString(420,680 - y,"Valor: " + str(missao.valor))
            valor_Final_Entrada_Misssao= valor_Final_Entrada_Misssao + missao.valor
        

        valorTotal = valor_Final_Entrada + valor_Final_Entrada_Avulsa + valor_Final_Entrada_Misssao
        pdf.setFont('Times-Bold', 14)
        pdf.drawString(325,640 - y,"Total Entrada: "+" R$ "+str(valor_Final_Entrada))
        pdf.drawString(325,620 - y,"Total Avulso: "+" R$ "+str(valor_Final_Entrada_Avulsa))
        pdf.drawString(325,600 - y,"Total Missões: "+" R$ "+str(valor_Final_Entrada_Misssao))
        pdf.drawString(325,580 - y,"Valor Total: "+" R$ "+str(valorTotal))
        
        pdf.save()
        nome = "relatorio_entrada.pdf"
        return render(request, 'index.html', {'nome': nome})
    else:
        congregacao = Congregacao.objects.all()
        return render(request, 'financeiro/form_relatorio.html', {'congregacao': congregacao})

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
                pdf.drawString(330,700 - y, str(entrada.categoria))
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
        
def gerarRelatorioGeral(request, entradas, saidas, missoes):
    data = str(date.today().strftime('%d/%m/%Y'))
    valorEntradas = 0
    valorEntradasAvulsa = 0
    valorMissao = 0
    valorTotalEntradas = 0
    valorTotalSaidas = 0
    y = 0
    pagina = False
    caminho = "ibc_financeiro/static/relatorio_geral.pdf"
    pdf = canvas.Canvas(caminho)
    pdf.setTitle("Relatório Geral")
    cabecalhoRelatorio(pdf, data)
    pdf.drawString(260,755,"Recebimentos")
    pdf.line(257, 752, 335, 752)
    pdf.setFont('Helvetica', 10)

    pdf.drawString(50, 700, 'Dizimos:............................................................................................ R$ ')
    pdf.drawString(365, 702, str(valorEntradas))
    pdf.line(363, 700, 550, 700)
    pdf.drawString(50, 680, 'Ofertas Avulsas:............................................................................... R$ ')
    pdf.drawString(365, 682 , str(valorEntradasAvulsa))
    pdf.line(363, 680, 550, 680)
    pdf.drawString(50, 660, 'Missões:........................................................................................... R$  ') 
    pdf.drawString(365, 662, str(valorMissao))
    pdf.line(363, 660, 550, 660)
    pdf.setFont('Times-Bold', 12)
    pdf.drawString(50, 642, 'Total de Entradas:................................................................. R$  ')
    pdf.drawString(365, 642, str(valorTotalEntradas))
    pdf.line(363, 640, 550, 640)
    pdf.drawString(260, 600, 'Pagamentos')
    pdf.line(257, 598, 325, 598)
    pdf.setFont('Helvetica', 10)
    for saida in range(1,len(saidas)+1): 
        y = y + 30
        valorTotalSaidas = valorTotalSaidas + saidas[saida - 1].valor
        if y > 500:
            y = 0
            pdf.showPage()
        if saida - 1 > 15:
            pagina = True
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
        pdf.setFont('Times-Bold', 12)
        pdf.drawString(50, 720 - y, 'Total de Saída:........................................................................ R$  ')
        pdf.drawString(365, 720 - y, str(valorTotalSaidas))
        pdf.line(363, 718 - y, 550, 718 - y)
    else:
        pdf.setFont('Times-Bold', 12)
        pdf.drawString(50, 555 - y, 'Total de Saída:........................................................................ R$  ')
        pdf.drawString(365, 557 - y, str(valorTotalSaidas))
        pdf.line(363, 555 - y, 550, 555 - y)
    pdf.drawString(20, 120, 'Conferido por: ')
    pdf.line(0, 100, 200, 100)
    pdf.line(210, 100, 400, 100)
    pdf.line(410, 100, 600, 100)
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
            listaMissao(request)

        return render(request, 'financeiro/paginas/relatorio.html', {'title' : tipo, 'formulario' : RelatorioMissaoForm()})

    elif tipo == 'geral':
        if request.method == 'POST':
            gerarRelatorioGeral(request, listaEntrada(request), listaSaida(request), listaMissao(request))
            return render(request, 'index.html', {'nome': 'relatorio_geral.pdf'})
        return render(request, 'financeiro/paginas/relatorio.html', {'title' : tipo, 'formulario' : RelatorioGeralForm()})

#Cabeçalhos Relatórios
def cabecalhoRelatorio(pdf, data):
    pdf.drawImage('ibc_financeiro/static/imagens/logo.png', 10,758,height=50, width=60)
    pdf.setFont('Times-Bold', 12)
    pdf.drawString(200,800,"IGREJA BATISTA DE CORRENTE")
    pdf.drawString(182,785,"Departamento de Administração e Finanças")
    pdf.drawString(240,770,"Relatório Financeiro")
    pdf.drawString(430,740,"Data: " + data)

# Métodos Auxiliares
def convertDate(date):
    return datetime.strptime(date, '%d/%m/%Y').date()

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

def listaGeral(request):
    entradas = listaEntrada(request)
    saidas = listaSaida(request)

    return list(chain(entradas, saidas))

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