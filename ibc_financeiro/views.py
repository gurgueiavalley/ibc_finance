from django.shortcuts import render
import pandas as pd
from . models import Membro
from decimal import Decimal

# Create your views here

def cadMembrosExcel(request):
    #Instalar o pandas
    #pip install pandas
    dados = pd.read_excel(r"C:\Users\Caike Silva\Desktop\membros.xlsx")
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
            membro.save()
    return render(request, 'index.html', {})
    

