import pytesseract
from PIL import Image
import csv
import os
from pdf2image import convert_from_path

# Set up Tesseract path if needed
# pytesseract.pytesseract.tesseract_cmd = r'<path_to_your_tesseract_executable>'

# Directory where your PDFs are stored
pdf_dir = 'invoice-2'

# CSV output file
csv_file = 'output-2.csv'

# Function to extract text from a PDF's first page
def extract_text_from_first_page(pdf_path):
    images = convert_from_path(pdf_path, first_page=1, last_page=1)
    text = pytesseract.image_to_string(images[0])
    return text

# Function to parse the OCR'd text and extract the desired information
def parse_text(text):
    lines = text.splitlines()
    # This is where you'll implement the logic to find the invoice details.
    # This will depend on the structure of the text.
    # For example:
    invoice_number = 'Not found'
    location = 'Not found'
    work_order_number = 'Not found'
    for line in lines:
        if 'INVOICE NUMBER:' in line:
            invoice_number = line.split(':')[-1].strip()
        elif 'LOCATION:' in line:
            location = line.split(':')[-1].strip()
        elif 'WORK ORDER #:' in line:
            work_order_number = line.split(':')[-1].strip()
    return invoice_number, location, work_order_number

# Open the CSV file for writing
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    # Write the header row
    writer.writerow(['INVOICE NUMBER', 'LOCATION', 'WORK ORDER #'])
    
    # Loop through all PDFs in the directory
    for filename in os.listdir(pdf_dir):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(pdf_dir, filename)
            text = extract_text_from_first_page(pdf_path)
            invoice_number, location, work_order_number = parse_text(text)
            # Write the data row
            writer.writerow([invoice_number, location, work_order_number])

print(f'Data has been written to {csv_file}')
