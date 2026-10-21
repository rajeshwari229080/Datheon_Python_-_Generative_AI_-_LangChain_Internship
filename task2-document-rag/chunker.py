"""
Task 2: Grounded Document Q&A Assistant (RAG)
Recursive character semantic text chunker with configurable overlap and metadata preservation.
"""

from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel, Field

from ingestion import DocumentPage


class DocumentChunk(BaseModel):
    """Represents a discrete semantic chunk of a document ready for vector embedding."""
    chunk_id: str = Field(..., description="Unique deterministic identifier e.g. 'doc.pdf_p1_c0'")
    source_file: str = Field(..., description="Originating document filename")
    page_number: int = Field(..., ge=1, description="Source page number")
    chunk_index: int = Field(..., ge=0, description="Sequential index within the document")
    text: str = Field(..., description="Textual payload of the chunk")
    char_count: int = Field(default=0, description="Character count")

    def model_post_init(self, __context) -> None:
        object.__setattr__(self, "char_count", len(self.text))


class RecursiveCharacterChunker:
    """
    Recursively splits text using a hierarchy of separators to preserve semantic context.
    Separators priority: Paragraphs ('\n\n') -> Lines ('\n') -> Sentences ('. ', '! ') -> Words (' ')
    """

    DEFAULT_SEPARATORS = ["\n\n", "\n", ". ", "? ", "! ", "; ", " ", ""]

    def __init__(
        self,
        chunk_size: int = 600,
        chunk_overlap: int = 120,
        separators: Optional[List[str]] = None
    ):
        if chunk_overlap >= chunk_size:
            raise ValueError(f"chunk_overlap ({chunk_overlap}) must be strictly less than chunk_size ({chunk_size})")

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separators = separators or self.DEFAULT_SEPARATORS

    def split_text(self, text: str) -> List[str]:
        """Splits an input string into overlapping chunks within character limits."""
        return self._recursive_split(text, self.separators)

    def _recursive_split(self, text: str, separators: List[str]) -> List[str]:
        final_chunks: List[str] = []
        separator = separators[-1]
        new_separators: List[str] = []

        for i, sep in enumerate(separators):
            if sep == "":
                separator = ""
                break
            if sep in text:
                separator = sep
                new_separators = separators[i + 1:]
                break

        splits = text.split(separator) if separator else list(text)

        good_splits: List[str] = []
        for s in splits:
            if not s:
                continue
            if len(s) < self.chunk_size:
                good_splits.append(s)
            else:
                if good_splits:
                    merged = self._merge_splits(good_splits, separator)
                    final_chunks.extend(merged)
                    good_splits = []
                if not new_separators:
                    final_chunks.append(s[:self.chunk_size])
                else:
                    other_chunks = self._recursive_split(s, new_separators)
                    final_chunks.extend(other_chunks)

        if good_splits:
            merged = self._merge_splits(good_splits, separator)
            final_chunks.extend(merged)

        return final_chunks

    def _merge_splits(self, splits: List[str], separator: str) -> List[str]:
        """Merges adjacent small splits while respecting chunk_size and chunk_overlap."""
        docs: List[str] = []
        current_doc: List[str] = []
        total = 0

        for d in splits:
            length = len(d) + (len(separator) if current_doc else 0)
            if total + length > self.chunk_size and current_doc:
                doc_text = separator.join(current_doc).strip()
                if doc_text:
                    docs.append(doc_text)
                
                # Keep tail items for overlap
                while total > self.chunk_overlap and current_doc:
                    removed = current_doc.pop(0)
                    total -= len(removed) + len(separator)

            current_doc.append(d)
            total += length

        if current_doc:
            doc_text = separator.join(current_doc).strip()
            if doc_text:
                docs.append(doc_text)

        return docs

    def chunk_document_pages(self, pages: List[DocumentPage]) -> List[DocumentChunk]:
        """Processes a list of DocumentPages into indexed DocumentChunks."""
        chunks: List[DocumentChunk] = []
        global_chunk_idx = 0

        for page in pages:
            raw_chunks = self.split_text(page.text)
            for idx, text_segment in enumerate(raw_chunks):
                if not text_segment.strip():
                    continue

                chunk_id = f"{page.source_file}_p{page.page_number}_c{idx}"
                chunks.append(DocumentChunk(
                    chunk_id=chunk_id,
                    source_file=page.source_file,
                    page_number=page.page_number,
                    chunk_index=global_chunk_idx,
                    text=text_segment
                ))
                global_chunk_idx += 1

        return chunks
