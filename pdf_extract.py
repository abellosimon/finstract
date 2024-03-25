import PyPDF2
import pandas as pd
from openpyxl import Workbook

def extract_text(pdf_path):
    text_pages = []
    with open(pdf_path, 'rb') as file:
        pdf = PyPDF2.PdfReader(file)
        for page in pdf.pages:
            text = page.extract_text()
            text_pages.append(text)
    return text_pages

def find_statements(text_pages, keywords):
    statements = {keyword: [] for keyword in keywords}
    for page in text_pages:
        for keyword in keywords:
            if keyword.lower() in page.lower():
                # Attempt to split page into lines and identify table-like structures
                lines = page.split('\n')
                for line in lines:
                    cells = line.split()  # Split line into cells based on whitespace
                    if len(cells) > 1:  # Assume a line with more than one cell might be part of a table
                        statements[keyword].append(cells)
    return statements

def export_to_xls(statements, output_path):
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        for title, table in statements.items():
            if table:  # Check if table is not empty
                df = pd.DataFrame(table)
                df.to_excel(writer, sheet_name=title[:31], index=False, header=False)

def process_pdf(pdf_path, output_path):
    keywords = ['Income Statement', 'Balance Sheet', 'Cash Flow Statement', 'Statement of Comprehensive Income']
    text_pages = extract_text(pdf_path)
    statements = find_statements(text_pages, keywords)
    export_to_xls(statements, output_path)

pdf_path = '.reports/2022 Annual Report RBI.pdf'  # Replace with your PDF file path
output_path = 'financial_statements.xlsx'  # Output XLS file
process_pdf(pdf_path, output_path)
