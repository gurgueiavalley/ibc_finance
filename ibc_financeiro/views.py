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
        pdf.drawImage('ibc_financeiro/static/images/logo.png', 10,780,height=50, width=60)
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

def relatorioSaida(request):
    if request.method == 'POST':
        saidas = Saida.objects.all().order_by('data')

        categorias = request.POST.getlist('categoria')
        empresas = request.POST.getlist('empresa')

        saidas = saidas.filter(categoria__nome__in = categorias) if categorias != [] else saidas
        saidas = saidas.filter(empresa__nome__in = empresas) if empresas != [] else saidas

    return render(request, 'financeiro/paginas/relatorio.html', {'formulario' : SaidaRelatorioForm()})



# from reportlab.platypus import SimpleDocTemplate
# from reportlab.platypus import Table
# from reportlab.lib import colors
# from reportlab.platypus import TableStyle

def relatorioSaida1(request):
    # Criando arquivo
    PDF = canvas.Canvas('relatorioSaida.pdf')
    PDF.setTitle('Relatório de Saída')

    # Desenhando coordenadas
    desenharCoordenadas(PDF)

    # Título
    PDF.setFont('Times-Bold', 16)
    PDF.drawCentredString(300, 770, 'Relatório de Saída')
    
    # Subtítulo
    PDF.setFillColorRGB(0, 0, 255)
    PDF.setFont('Times-Roman', 12)
    PDF.drawCentredString(290, 720, 'Relatório de Saída 2')

    # Linha
    PDF.line(30, 710, 550, 710)

    # Texto
    texto = PDF.beginText(40, 680)
    texto.setFont('Courier', 12)
    texto.setFillColor(colors.orange)
    texto.textLine('Primeira linha')
    texto.textLine('Segunda linha')
    PDF.drawText(texto)

    # Imagem
    PDF.drawInlineImage('ibc_financeiro/static/images/logo.png', 130, 400, height = 40, width = 40)

    # Salvando
    PDF.save()
    
    return render(request, 'financeiro/index.html')

def desenharCoordenadas(PDF):
    PDF.drawString(100, 810, 'x100')
    PDF.drawString(200, 810, 'x200')
    PDF.drawString(300, 810, 'x300')
    PDF.drawString(400, 810, 'x400')
    PDF.drawString(500, 810, 'x500')

    PDF.drawString(10, 100, 'y100')
    PDF.drawString(10, 200, 'y200')
    PDF.drawString(10, 300, 'y300')
    PDF.drawString(10, 400, 'y400')
    PDF.drawString(10, 500, 'y500')
    PDF.drawString(10, 600, 'y600')
    PDF.drawString(10, 700, 'y700')
    PDF.drawString(10, 800, 'y800')

def relatorioSaida2(request):
    # Dados
    dados = [
        ['Nome', 'Categoria', 'Data', 'Valor']
    ]
    
    saidas = Saida.objects.all()

    total = 0

    for saida in saidas:
        dados.append([saida.nome, saida.categoria, str(saida.data), 'R$ ' + str(saida.valor)])
        total = total + saida.valor

    dados.append(['', '', 'Total', 'R$ ' + str(total)])

    PDF = SimpleDocTemplate(
        'relatorioSaida.pdf',
        pagesize = letter
    )

    tabela = Table(dados)
    
    style = TableStyle([
        # ('BACKGROUND', (0, 0), (3, 0), colors.blue),
        # ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),

        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),

        ('FONTNAME', (0, 0), (-1, 0), 'Times-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 16),

        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),

        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),

        ('BOX', (0, 0), (-1, -1), 2, colors.black),

        ('LINEBEFORE', (1, 1), (2, -1), 2, colors.red),
        ('LINEABOVE', (0, 2), (-1, 2), 2, colors.green),

        ('GRID', (0, 0), (-1, -1), 2, colors.black),
    ])
    tabela.setStyle(style)

    elementos = []
    elementos.append(tabela)

    PDF.build(elementos)

    return render(request, 'financeiro/index.html')