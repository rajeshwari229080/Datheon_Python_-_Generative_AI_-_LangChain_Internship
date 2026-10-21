"""
Task 1 Test Suite: Extractor & Sanitizer
Tests multi-pass JSON sanitization, markdown fence extraction,
and deterministic mock extraction pipeline.
"""

import pytest
import sys
import os

# Add parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sanitizer import JSONSanitizer
from extractor import StructuredJSONExtractor


def test_sanitizer_markdown_fences():
    """Verify markdown fences and json tags are cleanly removed."""
    raw = '```json\n{"invoice_id": "INV-123", "subtotal": 100.0}\n```'
    clean = JSONSanitizer.clean(raw)
    assert clean == '{"invoice_id": "INV-123", "subtotal": 100.0}'


def test_sanitizer_conversational_preamble():
    """Verify conversational filler before and after JSON is stripped."""
    raw = 'Here is your extracted invoice object:\n\n{"invoice_id": "INV-999"}\n\nHope this helps!'
    clean = JSONSanitizer.clean(raw)
    assert clean == '{"invoice_id": "INV-999"}'


def test_sanitizer_trailing_commas():
    """Verify trailing commas before closing braces are healed."""
    raw = '{"name": "Alice", "skills": ["Python", "Docker",],}'
    clean = JSONSanitizer.clean(raw)
    assert clean == '{"name": "Alice", "skills": ["Python", "Docker"]}'


def test_mock_extractor_invoice():
    """Verify structured extraction of an invoice using the mock engine."""
    extractor = StructuredJSONExtractor(provider="mock")
    text = "Please pay INVOICE #INV-2024-5501 issued on 2024-11-20 for services rendered."
    result = extractor.extract(raw_text=text, schema_type="invoice")

    assert result.status == "success"
    assert result.schema_type == "invoice"
    assert result.is_mock is True
    assert result.latency_ms > 0
    assert hasattr(result.data, "invoice_id")
    assert result.data.invoice_id == "INV-2024-5501"


def test_mock_extractor_resume():
    """Verify structured extraction of a resume using the mock engine."""
    extractor = StructuredJSONExtractor(provider="mock")
    text = "Resume for Dr. Marcus Vance. Senior ML Systems Engineer with 10 years experience."
    result = extractor.extract(raw_text=text, schema_type="resume")

    assert result.status == "success"
    assert result.schema_type == "resume"
    assert result.is_mock is True
    assert hasattr(result.data, "candidate_name")
    assert "Marcus" in result.data.candidate_name
