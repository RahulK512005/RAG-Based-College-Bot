import os
from typing import List, Dict, Any
from pypdf import PdfReader
import docx

class DocumentExtractor:
    """Extracts text from PDF, DOCX, and TXT files, preserving page numbers where applicable."""

    @staticmethod
    def extract_from_file(file_path: str, filename: str) -> List[Dict[str, Any]]:
        """
        Extract text blocks with page numbers.
        Returns a list of dicts: [{"text": str, "page_number": int}]
        """
        ext = os.path.splitext(filename)[1].lower()

        if ext == ".pdf":
            return DocumentExtractor._extract_pdf(file_path)
        elif ext in [".docx", ".doc"]:
            return DocumentExtractor._extract_docx(file_path)
        elif ext in [".txt", ".md", ".csv"]:
            return DocumentExtractor._extract_txt(file_path)
        else:
            raise ValueError(f"Unsupported file format: {ext}. Supported formats are PDF, DOCX, TXT.")

    @staticmethod
    def _extract_pdf(file_path: str) -> List[Dict[str, Any]]:
        pages_content = []
        reader = PdfReader(file_path)
        
        for idx, page in enumerate(reader.pages):
            text = page.extract_text() or ""
            if text.strip():
                pages_content.append({
                    "text": text,
                    "page_number": idx + 1
                })
        
        if not pages_content:
            raise ValueError("No readable text found in PDF document.")
        return pages_content

    @staticmethod
    def _extract_docx(file_path: str) -> List[Dict[str, Any]]:
        doc = docx.Document(file_path)
        full_text = []
        for paragraph in doc.paragraphs:
            if paragraph.text.strip():
                full_text.append(paragraph.text)
        
        text = "\n\n".join(full_text)
        if not text.strip():
            raise ValueError("No readable text found in DOCX document.")
        return [{"text": text, "page_number": 1}]

    @staticmethod
    def _extract_txt(file_path: str) -> List[Dict[str, Any]]:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
        
        if not text.strip():
            raise ValueError("File is empty.")
        return [{"text": text, "page_number": 1}]
