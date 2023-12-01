import pytesseract
from pdf2image import convert_from_path
from PyPDF2 import PdfReader, PdfWriter

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

def find_and_merge_matching_pages(invoices_pdf_path, work_orders_pdf_path):
    invoices_reader = PdfReader(invoices_pdf_path)
    work_orders_reader = PdfReader(work_orders_pdf_path)

    for invoice_page_number in range(len(invoices_reader.pages)):
        invoice_text = extract_text_from_pdf_page(invoices_pdf_path, invoice_page_number)
        if not invoice_text:
            continue

        location_line = [line for line in invoice_text.split('\n') if "LOCATION: " in line]
        work_order_line = [line for line in invoice_text.split('\n') if "WORK ORDER #: " in line]

        if not location_line or not work_order_line:
            print(f"Required information not found on page {invoice_page_number} of invoices")
            continue

        location = location_line[0].split("LOCATION: ")[1].split()[0]
        work_order_number = work_order_line[0].split("WORK ORDER #: ")[1].split()[0]

        for work_order_page_number in range(len(work_orders_reader.pages)):
            work_order_text = extract_text_from_pdf_page(work_orders_pdf_path, work_order_page_number)
            if work_order_text and f"Work Order: {work_order_number}" in work_order_text:
                output_filename = f"{location}.pdf"
                merge_pdfs(invoices_pdf_path, invoice_page_number, work_orders_pdf_path, work_order_page_number, output_filename)
                break

# Paths to your PDF files
invoices_pdf_path = 'invoice-2-merged.pdf'
work_orders_pdf_path = 'wo_invoice-2.pdf'

find_and_merge_matching_pages(invoices_pdf_path, work_orders_pdf_path)
