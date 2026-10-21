"""
Task 1 Test Suite: Schemas Validation
Tests Pydantic v2 validation rules, line item calculations, currency normalization,
and error handling on invalid payloads.
"""

import pytest
from pydantic import ValidationError
import sys
import os

# Add parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from invoice_schema import InvoiceSchema, InvoiceLineItem, VendorInfo, ClientInfo
from resume_schema import ResumeSchema, WorkExperience, Education, SkillsInventory


def test_invoice_schema_valid():
    """Verify a properly formatted invoice validates successfully."""
    payload = {
        "invoice_id": "INV-2025-001",
        "invoice_date": "2025-01-15",
        "due_date": "2025-02-15",
        "currency": "USD",
        "vendor": {
            "name": "Apex Cloud Systems",
            "email": "billing@apexcloud.io",
            "tax_id": "US-123456"
        },
        "client": {
            "name": "Global Corp",
            "email": "ap@globalcorp.com"
        },
        "line_items": [
            {
                "description": "Cloud Compute Node",
                "quantity": 2.0,
                "unit_price": 500.0,
                "total_price": 1000.0
            },
            {
                "description": "Storage Volume",
                "quantity": 1.0,
                "unit_price": 200.0,
                "total_price": 200.0
            }
        ],
        "subtotal": 1200.0,
        "tax_amount": 100.0,
        "discount_amount": 50.0,
        "total_amount": 1250.0,
        "payment_terms": "Net 30"
    }
    model = InvoiceSchema.model_validate(payload)
    assert model.invoice_id == "INV-2025-001"
    assert model.total_amount == 1250.0
    assert len(model.line_items) == 2


def test_invoice_currency_normalization():
    """Verify currency symbols are normalized to ISO codes."""
    payload = {
        "invoice_id": "INV-100",
        "invoice_date": "2025-01-01",
        "currency": "$",
        "vendor": {"name": "Vendor A"},
        "client": {"name": "Client B"},
        "line_items": [{"description": "Item 1", "quantity": 1, "unit_price": 10, "total_price": 10}],
        "subtotal": 10.0,
        "tax_amount": 0.0,
        "total_amount": 10.0
    }
    model = InvoiceSchema.model_validate(payload)
    assert model.currency == "USD"


def test_invoice_line_item_auto_total():
    """Verify line item total is calculated if mismatched."""
    item = InvoiceLineItem(description="Service", quantity=4.0, unit_price=25.0, total_price=0.0)
    assert item.total_price == 100.0


def test_invoice_subtotal_consistency():
    """Verify subtotal synchronizes if sum of items deviates."""
    payload = {
        "invoice_id": "INV-200",
        "invoice_date": "2025-01-01",
        "currency": "EUR",
        "vendor": {"name": "Vendor A"},
        "client": {"name": "Client B"},
        "line_items": [
            {"description": "Item 1", "quantity": 1, "unit_price": 100.0, "total_price": 100.0},
            {"description": "Item 2", "quantity": 2, "unit_price": 50.0, "total_price": 100.0}
        ],
        "subtotal": 999.0, # Intentional mismatch
        "tax_amount": 0.0,
        "total_amount": 999.0
    }
    model = InvoiceSchema.model_validate(payload)
    assert model.subtotal == 200.0
    assert model.total_amount == 200.0


def test_resume_schema_valid():
    """Verify a valid candidate resume passes validation."""
    payload = {
        "candidate_name": "jane doe",
        "email": "jane.doe@example.com",
        "professional_summary": "Lead ML Engineer with expertise in PyTorch and LangChain.",
        "experience": [
            {
                "company": "Tech Corp",
                "job_title": "Senior Engineer",
                "start_date": "2021-01",
                "achievements": ["Deployed high-throughput vector store"]
            }
        ],
        "education": [
            {
                "institution": "MIT",
                "degree": "B.S. in Computer Science",
                "graduation_year": 2020
            }
        ],
        "skills": {
            "programming_languages": ["Python", "Go"],
            "frameworks_and_libraries": ["FastAPI", "PyTorch"]
        }
    }
    model = ResumeSchema.model_validate(payload)
    assert model.candidate_name == "Jane Doe" # Title cased
    assert model.email == "jane.doe@example.com"
    assert len(model.experience) == 1


def test_resume_invalid_name():
    """Verify short or invalid candidate names are rejected."""
    payload = {
        "candidate_name": " ",
        "email": "test@example.com",
        "professional_summary": "Summary here"
    }
    with pytest.raises(ValidationError):
        ResumeSchema.model_validate(payload)
