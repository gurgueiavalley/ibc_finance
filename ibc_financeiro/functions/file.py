import os
import fitz

from PyPDF2 import PdfFileMerger
from fpdf   import FPDF

from PIL import Image

class File():
    def delete(archives):
        for archive in archives:
            try:
                os.remove(archive)
                os.rmdir(archive.replace(archive.split('/')[-1], ''))
            
            except:
                pass

class PDF():
    def cover(pdf):
        pdf.add_page()
        
        pdf.ln(125)
        pdf.set_font('Helvetica', 'B', 36)
        pdf.cell(0, 12, 'Anexos', align = 'C')
        
        pdf.ln(12)
        pdf.set_font('', size = 16)
        pdf.cell(0, 7, 'Comprovantes', align = 'C')

    def footer(pdf, numberes, movement):        
        pdf.ln(265)
        pdf.set_font('', 'B', 16)
        width, height = 40, 7

        pdf.cell(width - 10, height, 'Linha')

        if numberes['part'] != None:
            pdf.cell(width - 10, height, 'Parte')   

        else:
            pdf.cell(width, height, 'Tipo')
            pdf.cell(width + 5, height, 'Método')

            if hasattr(movement, 'nome'):
                pdf.cell(width, height, 'Saída')

        pdf.ln(height)
        pdf.set_font('', '', 14)
        
        pdf.cell(width - 10, height, str(numberes['line']))

        if numberes['part'] != None:
            pdf.cell(width, height, numberes['part'])

        else:
            pdf.cell(width, height, 'Comprovante')
            pdf.cell(width + 5, height, movement.transacao.nome.title())

            if hasattr(movement, 'nome'):
                pdf.cell(width, height, movement.nome.title()[:30])

    def header(pdf, category):
        pdf.set_text_color(200)
        pdf.set_font('', 'B', 30)
        pdf.cell(0, 13, category.title()[:30], align = 'C')

    def merge(pdfs, final, name):
        pdf = PdfFileMerger()
        pdf.addMetadata({'/Title' : name})

        for p in pdfs:
            if p != '':
                pdf.append(p)

        pdf.write(final)
        pdf.close()

    def toPDF(data, final):
        pdf = FPDF()
        pdf.set_auto_page_break(auto = False)
        
        PDF.cover(pdf)

        number, part, categories = 0, 1, []
        
        for d in data:
            pdf.add_page()

            category = d['movement'].categoria.nome if hasattr(d['movement'], 'categoria') else 'Avulsa'

            if category not in categories:
                categories.append(category)

                PDF.header(pdf, category)

            width, height = Image.open(d['image']).size

            if width >= height:
                pdf.image(d['image'], x = 20, y = 50, w = 170)

            else:
                pdf.image(d['image'], x = 13, y = 30, h = 235)

            if d['number'] != number:
                PDF.footer(pdf, {
                    'line' : d['number'],
                    'part' : None
                }, d['movement'])
                
                number = d['number']
                part = 1

            else:
                part += 1

                PDF.footer(pdf, {
                    'line' : d['number'],
                    'part' : str(part)
                }, d['movement'])

        pdf.output(final)

    def toPNG(pdf):
        folder = pdf.replace('.pdf', '')

        if not os.path.isdir(folder):
            os.mkdir(folder)
        
        archive, images = fitz.open(pdf), []
        
        for page in range(archive.page_count):
            image = folder + '/' + str(page) + '.png'
            images.append(image)

            archive.loadPage(page).getPixmap().writePNG(image)

        return images