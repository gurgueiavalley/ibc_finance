from django.test import TestCase

# from reportlab.platypus import SimpleDocTemplate
# from reportlab.platypus import Table
# from reportlab.lib import colors
# from reportlab.platypus import TableStyle

# def relatorioSaida1(request):
    # Criando arquivo
    # PDF = canvas.Canvas('relatorioSaida.pdf')
    # PDF.setTitle('Relatório de Saída')

    # Desenhando coordenadas
    # desenharCoordenadas(PDF)

    # Título
    # PDF.setFont('Times-Bold', 16)
    # PDF.drawCentredString(300, 770, 'Relatório de Saída')
    
    # Subtítulo
    # PDF.setFillColorRGB(0, 0, 255)
    # PDF.setFont('Times-Roman', 12)
    # PDF.drawCentredString(290, 720, 'Relatório de Saída 2')

    # Linha
    # PDF.line(30, 710, 550, 710)

    # Texto
    # texto = PDF.beginText(40, 680)
    # texto.setFont('Courier', 12)
    # texto.setFillColor(colors.orange)
    # texto.textLine('Primeira linha')
    # texto.textLine('Segunda linha')
    # PDF.drawText(texto)

    # Imagem
    # PDF.drawInlineImage('ibc_financeiro/static/images/logo.png', 130, 400, height = 40, width = 40)

    # Salvando
    # PDF.save()
    
    # return render(request, 'financeiro/index.html')

# def desenharCoordenadas(PDF):
    # PDF.drawString(100, 810, 'x100')
    # PDF.drawString(200, 810, 'x200')
    # PDF.drawString(300, 810, 'x300')
    # PDF.drawString(400, 810, 'x400')
    # PDF.drawString(500, 810, 'x500')

    # PDF.drawString(10, 100, 'y100')
    # PDF.drawString(10, 200, 'y200')
    # PDF.drawString(10, 300, 'y300')
    # PDF.drawString(10, 400, 'y400')
    # PDF.drawString(10, 500, 'y500')
    # PDF.drawString(10, 600, 'y600')
    # PDF.drawString(10, 700, 'y700')
    # PDF.drawString(10, 800, 'y800')

# def relatorioSaida2(request):

    # dados = [
    #     ['Nome', 'Categoria', 'Data', 'Valor']
    # ]
    
    # saidas = Saida.objects.all()

    # total = 0

    # for saida in saidas:
    #     dados.append([saida.nome, saida.categoria, str(saida.data), 'R$ ' + str(saida.valor)])
    #     total = total + saida.valor

    # dados.append(['', '', 'Total', 'R$ ' + str(total)])

    # PDF = SimpleDocTemplate(
    #     'relatorioSaida.pdf',
    #     pagesize = letter
    # )

    # tabela = Table(dados)
    
    # style = TableStyle([
        # ('BACKGROUND', (0, 0), (3, 0), colors.blue),
        # ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),

    #     ('ALIGN', (0, 0), (-1, -1), 'CENTER'),

    #     ('FONTNAME', (0, 0), (-1, 0), 'Times-Bold'),
    #     ('FONTSIZE', (0, 0), (-1, 0), 16),

    #     ('BOTTOMPADDING', (0, 0), (-1, 0), 12),

    #     ('BACKGROUND', (0, 1), (-1, -1), colors.beige),

    #     ('BOX', (0, 0), (-1, -1), 2, colors.black),

    #     ('LINEBEFORE', (1, 1), (2, -1), 2, colors.red),
    #     ('LINEABOVE', (0, 2), (-1, 2), 2, colors.green),

    #     ('GRID', (0, 0), (-1, -1), 2, colors.black),
    # ])
    # tabela.setStyle(style)

    # elementos = []
    # elementos.append(tabela)

    # PDF.build(elementos)

    # return render(request, 'financeiro/index.html')

# saidas = Saida.objects.all().order_by('data')

# categorias = request.POST.getlist('categoria')
# empresas = request.POST.getlist('empresa')

# saidas = saidas.filter(categoria__nome__in = categorias) if categorias != [] else saidas
# saidas = saidas.filter(empresa__nome__in = empresas) if empresas != [] else saidask0