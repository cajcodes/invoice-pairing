import pytesseract
from pdf2image import convert_from_path
from PyPDF2 import PdfReader, PdfWriter
import os
import re
from concurrent.futures import ThreadPoolExecutor

def extract_text_from_pdf_page(pdf_path, page_number):
    try:
        page_image = convert_from_path(pdf_path, first_page=page_number+1, last_page=page_number+1)[0]
        return pytesseract.image_to_string(page_image)
    except IndexError:
        print(f"No page found for {page_number} in {pdf_path}")
        return None

def merge_pdfs(pdf1_path, pdf1_page_number, pdf2_path, pdf2_page_number, output_path):
    try:
        pdf1_reader = PdfReader(pdf1_path)
        pdf2_reader = PdfReader(pdf2_path)
        writer = PdfWriter()

        writer.add_page(pdf1_reader.pages[pdf1_page_number])
        writer.add_page(pdf2_reader.pages[pdf2_page_number])

        with open(output_path, 'wb') as output_pdf:
            writer.write(output_pdf)
    except IndexError as e:
        print(f"Error merging PDFs: {e}")

import re

def process_invoice_page(invoice_page_data):
    invoices_pdf_path, invoice_page_number, work_orders_pdf_path = invoice_page_data
    
    # Extract text from the invoice page
    invoice_text = extract_text_from_pdf_page(invoices_pdf_path, invoice_page_number)
    if not invoice_text:
        print(f"Text extraction failed for invoice page {invoice_page_number}")
        return

    # Use regular expression to find the full location line
    location_match = re.search(r'LOCATION:\s+(.*)', invoice_text)
    if location_match:
        full_location = location_match.group(1).strip()
        # Use the full location as part of the filename, replacing any characters that are invalid in filenames
        safe_filename = re.sub(r'[\\/:"*?<>|]+', "", full_location)
        output_filename = f"{safe_filename}.pdf"
    else:
        print(f"Location not found on invoice page {invoice_page_number}")
        return

    # Extract work order number from the invoice text
    work_order_line = [line for line in invoice_text.split('\n') if "WORK ORDER #:" in line]
    if not work_order_line:
        print(f"Work Order number not found on invoice page {invoice_page_number}")
        return

    work_order_number = work_order_line[0].split("WORK ORDER #: ")[1].split()[0]

    # Find the matching work order page
    work_orders_reader = PdfReader(work_orders_pdf_path)
    for work_order_page_number in range(len(work_orders_reader.pages)):
        work_order_text = extract_text_from_pdf_page(work_orders_pdf_path, work_order_page_number)
        if work_order_text and f"Work Order: {work_order_number}" in work_order_text:
            # Merge the invoice and work order pages into a new PDF with the location as the filename
            merge_pdfs(invoices_pdf_path, invoice_page_number, work_orders_pdf_path, work_order_page_number, output_filename)
            print(f"Merged invoice page {invoice_page_number} and work order page {work_order_page_number} into {output_filename}")
            break

def find_and_merge_matching_pages(invoices_pdf_path, work_orders_pdf_path):
    invoices_reader = PdfReader(invoices_pdf_path)
    invoice_pages_data = [(invoices_pdf_path, i, work_orders_pdf_path) for i in range(len(invoices_reader.pages))]

    with ThreadPoolExecutor() as executor: # max_workers=6 in ()
        executor.map(process_invoice_page, invoice_pages_data)

# Paths to your PDF files
invoices_pdf_path = 'invoice-2-osp_materials.pdf'
work_orders_pdf_path = 'wo_invoice-2.pdf'

find_and_merge_matching_pages(invoices_pdf_path, work_orders_pdf_path)
