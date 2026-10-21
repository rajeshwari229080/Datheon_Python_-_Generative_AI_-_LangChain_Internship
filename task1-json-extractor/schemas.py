"""
Task 1: Structured LLM Prompt Pipeline & JSON Extractor
Re-exports InvoiceSchema, ResumeSchema, and ExtractionEnvelope.
"""

from __future__ import annotations
from typing import Literal, Union, Dict, Any, List
from datetime import datetime, timezone
from pydantic import BaseModel, Field

from invoice_schema import InvoiceSchema, InvoiceLineItem, VendorInfo, ClientInfo
from resume_schema import ResumeSchema, WorkExperience, Education, SkillsInventory


class ExtractionEnvelope(BaseModel):
    schema_type: Literal["invoice", "resume"]
    status: Literal["success", "validation_failed", "fallback_applied"]
    provider_used: str
    is_mock: bool = False
    latency_ms: float
    raw_input_snippet: str
    data: Union[InvoiceSchema, ResumeSchema, Dict[str, Any]]
    validation_notes: List[str] = Field(default_factory=list)
    extracted_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
