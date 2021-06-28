import os
import fitz

from fpdf   import FPDF
from PyPDF2 import PdfFileMerger

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
        pdf.set_font('', size = 15)
        pdf.cell(0, 7, 'Comprovantes e Notas Fiscais', align = 'C')

    def footer(pdf, data):        
        pdf.ln(265)
        pdf.set_font('', 'B', 16)
        
        width, height = 30, 7

        pdf.cell(width, height, 'Página')
        pdf.cell(width, height, 'Linha')

        movement = data['movement']

        if 'part' in data:
            pdf.cell(width, height, 'Parte')   

        else:
            pdf.cell(width + 10, height, 'Tipo')
            pdf.cell(width + 15, height, 'Método')
            pdf.cell(width + 10, height, 'Saída') if hasattr(movement, 'nome') else None

        line = data['line']
        page = 1 if line < 20 else int((line / 20) + 1)
        line = line if line < 20 else (20 - ((20 * page) - line)) + 1

        pdf.ln(height)
        pdf.set_font('', '', 14)

        pdf.cell(width, height, str(page))
        pdf.cell(width, height, str(line))

        if 'part' in data:
            pdf.cell(width + 10, height, data['part'])

        else:
            pdf.cell(width + 10, height, 'Comprovante')
            pdf.cell(width + 15, height, movement.transacao.nome.title())
            pdf.cell(width + 10, height, movement.nome.title()[:30]) if hasattr(movement, 'nome') else None

    def header(pdf, category):
        pdf.set_text_color(200)
        pdf.set_font('', 'B', 30)

        pdf.cell(0, 13, category.title()[:30], align = 'C')
    
    def imageToPDF(images, directory):
        pdf = FPDF()
        pdf.set_auto_page_break(auto = False)
        
        PDF.cover(pdf)

        categories, l, part = [], 0, 1
        
        for image in images:
            pdf.add_page()

            movement = image['movement']
            category = movement.categoria.nome if hasattr(movement, 'categoria') else 'Avulsa'

            if category not in categories:
                categories += [category]

                PDF.header(pdf, category)

            img = image['directory']
            width, height = Image.open(img).size
            pdf.image(img, 13, 50, 170) if width >= height else pdf.image(img, 13, 30, h = 235)

            line = image['line']
            data = {
                'line'      : line,
                'movement'  : movement
            }

            if line != l:
                l = line
                part = 1

            else:
                part += 1
                data['part'] = str(part)

            PDF.footer(pdf, data)

        pdf.output(directory)

    def merge(pdfs, final, name):
        pdf = PdfFileMerger()
        pdf.addMetadata({'/Title' : name})

        for p in pdfs:
            if p != '':
                pdf.append(p)

        pdf.write(final)
        pdf.close()

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