import os
from typing import Optional
from PyPDF2 import PdfReader
from docx import Document
from PIL import Image
import pytesseract


class DocumentProcessor:
    """Verarbeitet verschiedene Dokumenttypen und extrahiert Text."""

    @staticmethod
    def extract_text(file_path: str, filename: str) -> Optional[str]:
        """
        Extrahiert Text aus verschiedenen Dokumenttypen.

        Unterstützt:
        - PDF (.pdf)
        - Word (.docx)
        - Bilder (.jpg, .jpeg, .png) - mit OCR

        Returns:
            Extrahierter Text oder None bei Fehler
        """
        ext = os.path.splitext(filename)[1].lower()

        try:
            if ext == '.pdf':
                return DocumentProcessor._extract_from_pdf(file_path)
            elif ext == '.docx':
                return DocumentProcessor._extract_from_docx(file_path)
            elif ext in ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']:
                return DocumentProcessor._extract_from_image(file_path)
            elif ext == '.txt':
                return DocumentProcessor._extract_from_txt(file_path)
            else:
                return f"Dateiformat {ext} wird nicht unterstützt."

        except Exception as e:
            print(f"Error extracting text from {filename}: {str(e)}")
            return None

    @staticmethod
    def _extract_from_pdf(file_path: str) -> str:
        """Extrahiert Text aus PDF."""
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()

    @staticmethod
    def _extract_from_docx(file_path: str) -> str:
        """Extrahiert Text aus Word-Dokument."""
        doc = Document(file_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text.strip()

    @staticmethod
    def _extract_from_image(file_path: str) -> str:
        """Extrahiert Text aus Bild mittels OCR."""
        try:
            image = Image.open(file_path)
            # Tesseract OCR mit Deutsch als Sprache
            text = pytesseract.image_to_string(image, lang='deu')
            return text.strip()
        except Exception as e:
            # Fallback ohne Spracheinstellung
            try:
                image = Image.open(file_path)
                text = pytesseract.image_to_string(image)
                return text.strip()
            except:
                return f"OCR-Fehler: {str(e)}"

    @staticmethod
    def _extract_from_txt(file_path: str) -> str:
        """Liest Text aus .txt Datei."""
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()


document_processor = DocumentProcessor()
