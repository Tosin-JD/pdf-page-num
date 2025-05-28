import io
import os
from PyPDF2 import PdfReader, PdfWriter, PdfMerger
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch


def int_to_roman(num):
    """Convert an integer to a Roman numeral (lowercase)."""
    val = [
        1000, 900, 500, 400,
        100, 90, 50, 40,
        10, 9, 5, 4, 1
    ]
    syms = [
        "m", "cm", "d", "cd",
        "c", "xc", "l", "xl",
        "x", "ix", "v", "iv", "i"
    ]
    roman = ''
    for i in range(len(val)):
        count = int(num / val[i])
        roman += syms[i] * count
        num -= val[i] * count
    return roman


def create_page_number_overlay(page_width, page_height, text):
    """Create a PDF with Roman numeral page number centered at the bottom."""
    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=(page_width, page_height))

    c.setFont("Helvetica", 12)

    x = page_width / 2
    y = 1 * inch  # 1 inch from bottom

    c.drawCentredString(x, y, text)
    c.save()
    packet.seek(0)
    return PdfReader(packet)


def add_roman_page_numbers(input_pdf, output_pdf):
    reader = PdfReader(input_pdf)
    writer = PdfWriter()

    for i, page in enumerate(reader.pages):
        if i == 0:
            # First page, no page number
            writer.add_page(page)
        else:
            roman_number = int_to_roman(i + 1)  # 2nd page = ii
            overlay_pdf = create_page_number_overlay(
                page.mediabox.width,
                page.mediabox.height,
                roman_number
            )
            overlay_page = overlay_pdf.pages[0]
            page.merge_page(overlay_page)
            writer.add_page(page)

    with open(output_pdf, "wb") as f:
        writer.write(f)


# Usage
input_path = "input.pdf"
output_path = "output_with_roman_pages.pdf"

add_roman_page_numbers(input_path, output_path)
