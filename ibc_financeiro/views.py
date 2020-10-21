from django.shortcuts import render

from .models import *
from .forms import *

import pandas as pd
from decimal import Decimal
import os
from reportlab.pdfgen import canvas
from django.conf import settings
from pathlib import Path
import datetime

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

def relatorio(request, tipo):
    if tipo == 'saida':
        listaSaidaFiltrada(request)

    return render(request, 'financeiro/paginas/relatorios/saida.html', {'formulario' : RelatorioSaidaForm})

def listaSaidaFiltrada(request):
    if request.method == 'POST':
        saidas = Saida.objects.all().order_by('data')

        categorias = request.POST.getlist('categoria')
        empresas = request.POST.getlist('empresa')

        saidas = saidas.filter(categoria__nome__in = categorias) if categorias != [] else saidas
        saidas = saidas.filter(empresa__nome__in = empresas) if empresas != [] else saidas