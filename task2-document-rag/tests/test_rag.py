"""
Task 2 Test Suite: Document Ingestion, Recursive Chunking, Vector Retrieval, and Abstention.
"""

import os
import sys
import pytest

# Add parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ingestion import DocumentIngestionEngine, DocumentPage
from chunker import RecursiveCharacterChunker, DocumentChunk
from retrieval import ResilientCosineVectorIndex
from rag_engine import GroundedRAGEngine


def test_document_ingestion_text(tmp_path):
    """Verify plaintext ingestion captures metadata correctly."""
    sample_file = tmp_path / "policy.txt"
    sample_file.write_text("Apex Travel Policy.\nAll flights must be economy.\nMeal per diem is $85.", encoding="utf-8")

    pages = DocumentIngestionEngine.load_file(str(sample_file))
    assert len(pages) == 1
    assert pages[0].source_file == "policy.txt"
    assert pages[0].page_number == 1
    assert "Meal per diem" in pages[0].text
    assert pages[0].char_count > 0


def test_recursive_chunker_size_and_overlap():
    """Verify recursive character chunker obeys size limits and retains overlap."""
    text = (
        "Paragraph One introduces the corporate policy rules in detail.\n\n"
        "Paragraph Two outlines specific travel restrictions for international journeys.\n\n"
        "Paragraph Three specifies hotel lodging rate limits across major metropolitan centers.\n\n"
        "Paragraph Four establishes expense filing deadlines within thirty days."
    )
    pages = [DocumentPage(source_file="test_doc.txt", page_number=1, total_pages=1, text=text)]
    chunker = RecursiveCharacterChunker(chunk_size=120, chunk_overlap=30)
    chunks = chunker.chunk_document_pages(pages)

    assert len(chunks) > 1
    for chunk in chunks:
        assert chunk.char_count <= 150 # Reasonable boundary around separator
        assert chunk.source_file == "test_doc.txt"
        assert chunk.page_number == 1


def test_vector_retrieval_ranking():
    """Verify vector index accurately ranks most relevant chunks top."""
    chunks = [
        DocumentChunk(chunk_id="c0", source_file="doc.txt", page_number=1, chunk_index=0, text="Employees can book flights in economy class for domestic travel."),
        DocumentChunk(chunk_id="c1", source_file="doc.txt", page_number=1, chunk_index=1, text="Breakfast allowance is 20 dollars and dinner allowance is 40 dollars."),
        DocumentChunk(chunk_id="c2", source_file="doc.txt", page_number=2, chunk_index=2, text="Database backups must be encrypted with AES 256 KMS keys.")
    ]
    index = ResilientCosineVectorIndex()
    index.index_chunks(chunks)

    results = index.similarity_search("What is the dinner allowance?", top_k=2)
    assert len(results) > 0
    assert results[0].chunk.chunk_id == "c1"
    assert "dinner" in results[0].chunk.text.lower()
    assert results[0].similarity_score > 0.20


def test_grounded_rag_answer_and_citations(tmp_path):
    """Verify Grounded RAG produces grounded response with source page citations."""
    sample_file = tmp_path / "travel_guide.txt"
    sample_file.write_text(
        "Apex Travel Reimbursement Guide.\n"
        "The daily meal per diem allowance is strictly set to 85 dollars for domestic journeys.\n"
        "Receipts are mandatory for all transactions exceeding 25 dollars.",
        encoding="utf-8"
    )

    engine = GroundedRAGEngine(provider="mock")
    engine.ingest_document(str(sample_file))

    resp = engine.answer_question("What is the daily meal per diem allowance?")
    assert not resp.is_abstention
    assert "85 dollars" in resp.answer
    assert len(resp.citations) > 0
    assert resp.citations[0].source_file == "travel_guide.txt"
    assert resp.citations[0].page_number == 1


def test_strict_abstention_on_unsupported_query(tmp_path):
    """Verify Grounded RAG strictly abstains when question is not supported by documents."""
    sample_file = tmp_path / "travel_guide.txt"
    sample_file.write_text("Only economy flights are permitted under 5 hours.", encoding="utf-8")

    engine = GroundedRAGEngine(provider="mock")
    engine.ingest_document(str(sample_file))

    resp = engine.answer_question("What is the corporate policy on submarine travel to the Mariana Trench?")
    assert resp.is_abstention
    assert engine.ABSTENTION_MESSAGE in resp.answer
    assert len(resp.citations) == 0
