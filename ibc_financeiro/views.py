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

# Create your views here


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
        valor_Final = 0;
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

def index(request):
    return render(request, 'financeiro/index.html')
 