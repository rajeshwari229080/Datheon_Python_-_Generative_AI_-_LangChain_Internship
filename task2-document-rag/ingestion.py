"""
Task 2: Grounded Document Q&A Assistant (RAG)
Document Ingestion module for PDF, Markdown, and Plaintext files with page-level metadata tracking.
"""

from __future__ import annotations
import os
import re
from typing import List, Optional
from pydantic import BaseModel, Field


class DocumentPage(BaseModel):
    """Represents a single page or section extracted from an input document."""
    source_file: str = Field(..., description="Original filename or path of the document")
    page_number: int = Field(default=1, ge=1, description="1-indexed page number (or 1 for text files)")
    total_pages: int = Field(default=1, ge=1, description="Total pages in the source document")
    text: str = Field(..., description="Extracted textual content")
    char_count: int = Field(default=0, description="Length of normalized text")

    def model_post_init(self, __context) -> None:
        object.__setattr__(self, "char_count", len(self.text))


class DocumentIngestionEngine:
    """Extracts raw text and metadata from supported file formats."""

    SUPPORTED_EXTENSIONS = {".pdf", ".txt", ".md"}

    @staticmethod
    def clean_text(raw_text: str) -> str:
        """Normalizes whitespaces, carriage returns, and control characters."""
        text = raw_text.replace("\r\n", "\n").replace("\r", "\n")
        # Collapse excessive blank lines
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip()

    @classmethod
    def load_file(cls, filepath: str) -> List[DocumentPage]:
        """Loads a document and returns a list of DocumentPage objects."""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Document file not found at: {filepath}")

        ext = os.path.splitext(filepath)[1].lower()
        if ext not in cls.SUPPORTED_EXTENSIONS:
            raise ValueError(f"Unsupported file format '{ext}'. Supported: {cls.SUPPORTED_EXTENSIONS}")

        filename = os.path.basename(filepath)

        if ext == ".pdf":
            return cls._load_pdf(filepath, filename)
        else:
            return cls._load_plaintext(filepath, filename, ext)

    @classmethod
    def _load_pdf(cls, filepath: str, filename: str) -> List[DocumentPage]:
        """Extracts text page-by-page from a PDF document using pypdf."""
        import pypdf
        pages: List[DocumentPage] = []

        with open(filepath, "rb") as f:
            reader = pypdf.PdfReader(f)
            total_pages = len(reader.pages)

            for idx, page in enumerate(reader.pages):
                extracted = page.extract_text() or ""
                cleaned = cls.clean_text(extracted)
                if cleaned:
                    pages.append(DocumentPage(
                        source_file=filename,
                        page_number=idx + 1,
                        total_pages=total_pages,
                        text=cleaned
                    ))

        if not pages:
            # Fallback for empty or scanned PDF
            pages.append(DocumentPage(
                source_file=filename,
                page_number=1,
                total_pages=1,
                text=f"[Empty or image-only PDF document: {filename}]"
            ))

        return pages

    @classmethod
    def _load_plaintext(cls, filepath: str, filename: str, ext: str) -> List[DocumentPage]:
        """Loads a plaintext or markdown file as a single logical document."""
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            raw_content = f.read()

        cleaned = cls.clean_text(raw_content)
        return [DocumentPage(
            source_file=filename,
            page_number=1,
            total_pages=1,
            text=cleaned
        )]
