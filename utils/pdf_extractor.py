"""
pdf_extractor.py
----------------
Extracts text content from uploaded PDF resume files using PyPDF2.
"""

from PyPDF2 import PdfReader


def extract_text_from_pdf(pdf_path):
    """
    Read a PDF file and extract all text from every page.

    Args:
        pdf_path (str): Path to the PDF file on disk.

    Returns:
        str: Combined text from all pages of the PDF.
    """
    text = ""

    try:
        reader = PdfReader(pdf_path)

        # Loop through each page and extract text
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    except Exception as e:
        print(f"Error reading PDF '{pdf_path}': {e}")
        return ""

    return text.strip()
