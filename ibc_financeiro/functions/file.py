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
    def merge(pdfs, final):
        pdf = PdfFileMerger()

        for p in pdfs:
            if p != '':
                pdf.append(p)

        pdf.write(final)
        pdf.close()

    def toPDF(images, final):
        pdf = FPDF()

        for image in images:
            pdf.add_page()

            width, height = Image.open(image).size

            if width >= height:
                pdf.image(image, x = 20, y = 50, w = 170)

            else:
                pdf.image(image, x = 15, y = 30, h = 235)

        pdf.output(final)

    def toPNG(pdf):
        archive, images = fitz.open(pdf), []

        folder = pdf.replace('.pdf', '')
        os.mkdir(folder)
        
        for page in range(archive.page_count):
            image = folder + '/' + str(page) + '.png'
            images.append(image)

            archive.loadPage(page).getPixmap().writePNG(image)

        return images