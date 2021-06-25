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
        
        pdf.set_font('Helvetica', 'B', 36)
        pdf.cell(0, 250, 'Anexos', align = 'C')
        
        pdf.ln(10)
        
        pdf.set_font('', size = 16)
        pdf.cell(0, 250, 'Comprovantes', align = 'C')

    def merge(pdfs, final):
        pdf = PdfFileMerger()

        for p in pdfs:
            if p != '':
                pdf.append(p)

        pdf.write(final)
        pdf.close()

    def toPDF(images, final):
        pdf = FPDF()
        
        PDF.cover(pdf)

        for image in images:
            pdf.add_page()

            width, height = Image.open(image).size

            if width >= height:
                pdf.image(image, x = 20, y = 50, w = 170)

            else:
                pdf.image(image, x = 15, y = 30, h = 235)

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