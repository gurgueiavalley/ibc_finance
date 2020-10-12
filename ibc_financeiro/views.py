from django.shortcuts import render
import pandas as pd
from . models import Membro
from decimal import Decimal
from ibc_financeiro.forms import FormExcel
import os
from ibc_financeiro.models import Entrada, Excel
from reportlab.pdfgen import canvas
from django.conf import settings
from pathlib import Path

from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table
from reportlab.platypus import TableStyle

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
        valor_Final = 0
        y = 0
        caminho = "ibc_financeiro/static/relatorio_entrada.pdf"
        pdf = canvas.Canvas(caminho)
        pdf.setTitle("Relatório de Entradas")
        pdf.drawImage('ibc_financeiro/static/images/logo.png', 10,780,height=50, width=60)
        pdf.setFont('Times-Bold', 24)
        pdf.drawString(200,800,"Relatório de Entradas")
        pdf.setFont('Helvetica', 12)

        for entrada in Entrada.objects.filter(data__range=[request.POST['dataInicio'], request.POST['dataFim']]).order_by('data'):
            y = y + 20
            if(y > 500):
                y = 0
                pdf.showPage()
            pdf.drawString(100, 750 - y, "Data: " +  str(entrada.data))
            pdf.drawString(420,750 - y,"Valor: " + str(entrada.valor))
            valor_Final = valor_Final + entrada.valor
        pdf.drawString(420,720 - y,"Valor Total: "+str(valor_Final))
        pdf.save()
        nome = 'relatorio_entrada.pdf'
        return render(request, 'index.html', {'nome': nome})
    else:
        return render(request, 'financeiro/form_relatorio.html', {})



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

def relatorioSaida(request):
    # Dados
    dados = [
        ['Nome', 'Valor'],
        ['Monitor', 'R$800,00'],
        ['Cadeira', 'R$320,00'],
        ['SSD', 'R$260,00'],
    ]
    
    PDF = SimpleDocTemplate(
        'relatorioSaida.pdf',
        pagesize = letter
    )

    tabela = Table(dados)
    
    style = TableStyle([
        ('BACKGROUND', (0, 0), (3, 0), colors.blue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),

        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),

        ('FONTNAME', (0, 0), (-1, 0), 'Times-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 13),

        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),

        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),

        ('BOX', (0, 0), (-1, -1), 2, colors.black),

        ('LINEBEFORE', (1, 1), (2, -1), 2, colors.red),
        ('LINEABOVE', (0, 2), (-1, 2), 2, colors.green),

        ('GRID', (0, 1), (-1, -1), 2, colors.black),
    ])
    tabela.setStyle(style)

    elementos = []
    elementos.append(tabela)

    PDF.build(elementos)

    return render(request, 'financeiro/index.html')
