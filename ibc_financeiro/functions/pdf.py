from fpdf import FPDF
from PyPDF2 import PdfFileMerger

from PIL import Image
import os

class PDF():
    def convert(images, final):
        pdf = FPDF()

        for image in images:
            pdf.add_page()

            width, height = Image.open(image).size

            if width >= height:
                pdf.image(image, x = 20, y = 50, w = 170)

            else:
                pdf.image(image, x = 15, y = 30, h = 235)

        pdf.output(final)

    def merge(pdfs, final):
        pdf = PdfFileMerger()

        for p in pdfs:
            pdf.append(p)

        pdf.write(final)
        pdf.close()
    
    def delete(pdfs):
        for pdf in pdfs:
            os.remove(pdf)