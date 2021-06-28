from reportlab.platypus                     import SimpleDocTemplate, Table
from reportlab.lib.pagesizes                import A4
from reportlab.graphics.charts.piecharts    import Pie
from reportlab.graphics.shapes              import Drawing, String

from .file      import PDF, File
from itertools  import chain

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
    def receipt(movements, old, new, name):
        line, lines = 1, {}
        movements1, movements2 = [], []

        for movement in movements:
            index = '{}:{}'.format(movement.__class__.__name__, str(movement.id))
            lines[index] = line
            line += 1

            movements1.append(movement) if hasattr(movement, 'categoria') else movements2.append(movement)

        categories = []

        for movement in movements1:
            category = movement.categoria.nome
            categories.append(category) if category not in categories else None

        movements = []

        for category in categories:
            for movement in movements1:
                movements.append(movement) if movement.categoria.nome == category else None

        movements = list(chain(movements, movements2))

        receipts, delete = [], [old]

        for movement in movements:
            directory = 'media/' + str(movement.comprovante)

            if directory != 'media/':
                images = []

                if directory[-4:] == '.pdf':
                    images = PDF.toPNG(directory)
                    delete += images

                else:
                    images = [directory]

                index = '{}:{}'.format(movement.__class__.__name__, str(movement.id))

                for image in images:
                    receipts.append({
                        'directory' : image,
                        'line'      : lines[index],
                        'movement'  : movement
                    })
                
        receipt = ''

        if receipts != []:
            receipt = 'ibc_financeiro/static/receipt.pdf'
            PDF.imageToPDF(receipts, receipt)
            delete += [receipt]
        
        PDF.merge([old, receipt], new, name)
        
        File.delete(delete)