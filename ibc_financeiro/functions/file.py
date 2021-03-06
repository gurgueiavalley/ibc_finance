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

    def footer(pdf, data, options):        
        pdf.ln(265)
        pdf.set_font('', 'B', 16)
        
        width, height = 30, 7

        if 'pageLine' not in options:
            pdf.cell(width, height, 'Página') if 'page' not in options else None
            pdf.cell(width, height, 'Linha')

        movement = data['movement']

        pdf.cell(width + 10, height, 'Tipo')

        if 'part' in data:
            pdf.cell(width, height, 'Parte')   

        else:
            pdf.cell(width + 15, height, 'Método')
            pdf.cell(width + 10, height, 'Saída') if hasattr(movement, 'nome') else None
            
            if 'pageLine' in options and 'page' not in options:
                pdf.cell(width, height, 'Missão')

        pdf.ln(height)
        pdf.set_font('', '', 14)
        
        if 'pageLine' not in options:
            line = data['line']

            if 'page' not in options:
                page = 1 if line < 20 else int((line / 20) + 1)
                line = line if line < 20 else (20 - ((20 * page) - line)) + 1

                pdf.cell(width, height, str(page))
                
            pdf.cell(width, height, str(line))

        pdf.cell(width + 10, height, data['type'])

        if 'part' in data:
            pdf.cell(width + 10, height, data['part'])

        else:
            pdf.cell(width + 15, height, movement.transacao.nome.title())
            pdf.cell(width + 10, height, movement.nome.title()[:(32 if 'page' in options else 17)]) if hasattr(movement, 'nome') else None
            
            if 'pageLine' in options and 'page' not in options:
                pdf.cell(width, height, movement.missao.nome.title()[:37])

    def header(pdf, category):
        pdf.set_font('', 'B', 30)

        pdf.cell(0, 13, category.title()[:30], align = 'C')
    
    def imageToPDF(images, directory, options):
        pdf = FPDF()
        pdf.set_auto_page_break(auto = False)
        
        PDF.cover(pdf)

        categories, typeR, l, part = [], '', 0, 1
        
        for image in images:
            pdf.add_page()

            movement = image['movement']
            
            if movement.__class__.__name__ != 'EntradaMissao':
                category = movement.categoria.nome if hasattr(movement, 'categoria') else 'Avulsa'

                if category not in categories:
                    categories += [category]

                    PDF.header(pdf, category)

            img = image['directory']
            width, height = Image.open(img).size
            pdf.image(img, 13, 50, 170) if width >= height else pdf.image(img, 10, 30, h = 230)

            line, typeReceipt = image['line'], image['type']
            data = {
                'line'      : line,
                'type'      : typeReceipt,
                'movement'  : movement
            }
 
            if typeReceipt != typeR or line != l:
                typeR, l, part = typeReceipt, line, 1

            else:
                part += 1
                data['part'] = str(part)

            PDF.footer(pdf, data, options)

        pdf.output(directory)

    def merge(pdfs, final, name = None):
        pdf = PdfFileMerger()
        pdf.addMetadata({'/Title' : name}) if name != None else None

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