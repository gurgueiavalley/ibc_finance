from reportlab.platypus                     import SimpleDocTemplate, Table
from reportlab.lib.pagesizes                import A4
from reportlab.graphics.charts.piecharts    import Pie
from reportlab.graphics.shapes              import Drawing, String

from .file import *

class Chart():
    def pie(saidas):
        archive = 'ibc_financeiro/static/chart.pdf'

        PDF = SimpleDocTemplate(archive, pagesize = A4)

        categories, totais = [], []

        for saida in saidas:
            if saida.categoria.nome not in categories:
                categories.append(saida.categoria.nome)
        
        for category in categories:
            total = 0

            for saida in saidas:
                if category == saida.categoria.nome:
                    total += saida.valor

            totais.append(int(total))

        title = String(55, 300, 'Gráficos', fontSize = 24, fontName = 'Times-Bold')
        subtitle = String(30, 255, 'Categorias de Saída', fontSize = 16, fontName = 'Times-Bold')

        chart = Pie()
        chart.data, chart.labels = totais, categories
        chart.sideLabels = True
        chart.height, chart.width = 200, 200

        drawing = Drawing(240, 120)
        drawing.add(title)
        drawing.add(subtitle)
        drawing.add(chart)

        table = Table([[drawing]], 215, 300)

        PDF.build([table])

    def progress(pdf, meta, total, y):
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

            if comeco == 499:
                break

        pdf.setStrokeColorRGB(1, 0, 0)

        for x in range(comeco + 1, 500):
            pdf.line(x, y - 5.5, x, y - 24.5)
            pdf.line(x + 0.5, y - 5.5, x, y - 24.5)

        pdf.setStrokeColorRGB(0, 0, 1)

        comeco = 100

        if meta < total:
            for x in range(comeco + 1, 500):
                pdf.line(x, y - 5.5, x, y - 24.5)
                pdf.line(x + 0.5, y - 5.5, x, y - 24.5)
           
        pdf.setStrokeColorRGB(0,0,0)
        
        pdf.line(500, y - 5, 500, y - 25) 
        pdf.line(100, y - 25, 500, y - 25)


        pdf.drawString(100, y - 38, 'Alcançado: R$ ' + '{:.2f}'.format(total))

        if meta > total:
            pdf.drawString(383, y - 38, 'Restante: R$ ' + '{:.2f}'.format(meta - total))

        else:
            pdf.drawString(383, y - 38, 'Ultrapassado: R$ ' + '{:.2f}'.format(total - meta))

class Report():
    def receipt(movements, old, new):
        receipts, remove, receipt, number = [], [old], '', 1

        for movement in movements:
            directory = str(movement.comprovante)

            if directory != '':
                if directory[-4:] == '.pdf':
                    images = PDF.toPNG('media/' + directory)

                    for image in images:
                        receipts.append({
                            'number' : number,
                            'image' : image,
                            'movement' : movement
                        })

                    remove += images
                
                else:
                    receipts.append({
                        'number' : number,
                        'image' : 'media/' + directory,
                        'movement' : movement
                    })

            number += 1

        if receipts != []:
            receipt = 'ibc_financeiro/static/receipt.pdf'
            PDF.toPDF(receipts, receipt)
            remove.append(receipt)
        
        PDF.merge([old, receipt], new)
        
        File.delete(remove)