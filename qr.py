import qrcode
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
from reportlab.lib.utils import ImageReader
import io

def generate_qr_pdf(student_number, output_pdf):
    """
    Generate a PDF with each QR code on a separate page.

    :param data_list: List of data strings to encode into QR codes.
    :param output_pdf: Path to the output PDF file.
    """
    # Create a canvas for the PDF
    c = canvas.Canvas(output_pdf, pagesize=letter)
    width, height = letter

    data_list = [n for n in range(student_number)]
    for data in data_list:
        qr = qrcode.QRCode()
        qr.add_data(data)  # Add unique data for this QR code
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")
        img_buffer = io.BytesIO()
        qr_img.save(img_buffer)
        img_buffer.seek(0) 
        qr_size = 800  # Size of the QR code on the page
        x = (width - qr_size) / 2  # Center the QR code horizontally
        y = (height - qr_size) / 2  # Center the QR code vertically
        c.drawImage(ImageReader(img_buffer), x, y, qr_size, qr_size)
        c.showPage()

    # Save the PDF
    c.save()
