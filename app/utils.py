import pdfplumber
from typing import List, Dict
import io

def extract_text_from_pdf(pdf_bytes: bytes) -> Dict[int, str]:
    """
    Extracts text from a PDF file provided as bytes.
    Returns a dictionary mapping page number (1-indexed) to text content.
    """
    text_map = {}
    try:
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            for i, page in enumerate(pdf.pages):
                text = page.extract_text()
                if text:
                    text_map[i + 1] = text
                else:
                    text_map[i + 1] = "[NO TEXT EXTRACTED]" 
    except Exception as e:
        print(f"Error extracting PDF: {e}")
        return {1: f"Error reading PDF: {str(e)}"}
        
    return text_map

def get_pages_for_type(classifications: List[dict], doc_type: str) -> List[int]:
    """
    Returns a list of page numbers classified as a specific document type.
    """
    return [c['page_number'] for c in classifications if c['document_type'] == doc_type]
