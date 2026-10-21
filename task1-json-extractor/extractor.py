"""
Task 1: Structured LLM Prompt Pipeline & JSON Extractor
Core Extractor engine supporting Gemini, OpenAI, and Deterministic Mock fallback,
with multi-pass JSON sanitization and Pydantic v2 validation.
"""

from __future__ import annotations
import os
import re
import json
import time
from typing import Dict, Any, Optional, Tuple, Type
from pydantic import ValidationError, BaseModel
from dotenv import load_dotenv

from schemas import InvoiceSchema, ResumeSchema, ExtractionEnvelope
from prompts import build_extraction_prompt, build_healing_prompt
from sanitizer import JSONSanitizer

load_dotenv()


class ExtractionError(Exception):
    """Raised when extraction fails completely after retry attempts."""
    pass


class LLMClient:
    """Handles communication with Google Gemini, OpenAI, or the offline Mock engine."""

    def __init__(self, provider: Optional[str] = None):
        self.provider = (provider or os.getenv("DEFAULT_LLM_PROVIDER", "mock")).lower()
        self.gemini_key = os.getenv("GEMINI_API_KEY", "")
        self.openai_key = os.getenv("OPENAI_API_KEY", "")

    def generate(self, prompt: str) -> Tuple[str, str, bool]:
        """
        Executes generation against configured provider.
        Returns: (raw_response_text, provider_name, is_mock_flag)
        """
        if self.provider == "gemini" and self.gemini_key and not self.gemini_key.startswith("your_"):
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.gemini_key)
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(prompt)
                return response.text, "google-gemini-1.5-flash", False
            except Exception:
                pass

        if self.provider == "openai" and self.openai_key and not self.openai_key.startswith("your_"):
            try:
                from openai import OpenAI
                client = OpenAI(api_key=self.openai_key)
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.1,
                )
                return response.choices[0].message.content or "", "openai-gpt-4o-mini", False
            except Exception:
                pass

        # Deterministic Mock Provider (Zero API Keys Required)
        return self._generate_deterministic_mock(prompt), "deterministic-offline-mock", True

    def _generate_deterministic_mock(self, prompt: str) -> str:
        """Parses the document portion of the prompt to generate a schema-valid response."""
        # Isolate the current document text from few-shot exemplars
        doc_text = prompt
        if "### Current Document to Extract:" in prompt:
            doc_text = prompt.split("### Current Document to Extract:")[-1]

        if "InvoiceSchema" in prompt or "line_items" in prompt:
            inv_match = re.search(r"INV[-\d]+", doc_text, re.IGNORECASE)
            inv_id = inv_match.group(0) if inv_match else "INV-2024-9102"

            return json.dumps({
                "invoice_id": inv_id,
                "invoice_date": "2024-11-20",
                "due_date": "2024-12-20",
                "currency": "USD",
                "vendor": {
                    "name": "Apex Cloud Systems",
                    "tax_id": "US-88992144",
                    "email": "billing@apexcloud.io",
                    "phone": "+1 (415) 555-0199",
                    "address": "450 Mission Street, San Francisco, CA"
                },
                "client": {
                    "name": "Global Data Enterprises",
                    "email": "invoices@globaldata.com",
                    "phone": "+1 (212) 555-8821",
                    "address": "742 Evergreen Terrace, Springfield, OR"
                },
                "line_items": [
                    {
                        "description": "Production GPU Compute Nodes (8x H100)",
                        "quantity": 2.0,
                        "unit_price": 4200.0,
                        "total_price": 8400.0
                    },
                    {
                        "description": "Distributed Storage Volume (50 TB NVMe)",
                        "quantity": 1.0,
                        "unit_price": 1250.0,
                        "total_price": 1250.0
                    }
                ],
                "subtotal": 9650.0,
                "tax_amount": 772.0,
                "discount_amount": 150.0,
                "total_amount": 10272.0,
                "payment_terms": "Net 30"
            }, indent=2)
        else:
            name_match = re.search(r"(?:Name:\s*|Dr\.\s*|Mr\.\s*)([A-Z][a-z]+ [A-Z][a-z]+)", doc_text)
            cand_name = name_match.group(1) if name_match else "Marcus Aurelius Vance"

            return json.dumps({
                "candidate_name": cand_name,
                "email": "marcus.vance@apexai.internal",
                "phone": "+1 (650) 555-4321",
                "location": "Seattle, WA",
                "linkedin_url": "https://linkedin.com/in/marcusvance",
                "github_url": "https://github.com/marcusvance",
                "professional_summary": "Distinguished Machine Learning Platform Engineer with 9 years of experience designing real-time vector search backends and high-concurrency microservices.",
                "experience": [
                    {
                        "company": "Apex Distributed Labs",
                        "job_title": "Lead Infrastructure Architect",
                        "start_date": "2021-03",
                        "end_date": "Present",
                        "location": "Seattle, WA",
                        "achievements": [
                            "Engineered distributed indexing system for 200M embeddings with <15ms retrieval latency.",
                            "Automated model deployment pipelines using Kubernetes and Triton Inference Server."
                        ],
                        "skills_used": ["Python", "Go", "Kubernetes", "PyTorch", "gRPC", "Triton"]
                    }
                ],
                "education": [
                    {
                        "institution": "University of Washington",
                        "degree": "M.S. in Computer Science",
                        "field_of_study": "Distributed Systems",
                        "graduation_year": 2018,
                        "gpa": "3.92"
                    }
                ],
                "skills": {
                    "programming_languages": ["Python", "Rust", "Go", "C++", "SQL"],
                    "frameworks_and_libraries": ["FastAPI", "Pydantic", "PyTorch", "Ray", "Docker"],
                    "cloud_and_devops": ["AWS", "Kubernetes", "Terraform", "Prometheus", "Kafka"],
                    "databases": ["PostgreSQL", "ChromaDB", "Redis", "Pinecone"],
                    "tools_and_methods": ["Microservices Architecture", "Vector Search Optimization"]
                },
                "certifications": ["AWS Certified Solutions Architect - Professional"]
            }, indent=2)


class StructuredJSONExtractor:
    """Orchestrates prompt formatting, LLM generation, multi-pass healing, and Pydantic validation."""

    def __init__(self, provider: Optional[str] = None, max_retries: int = 2):
        self.client = LLMClient(provider=provider)
        self.max_retries = max_retries

    def extract(self, raw_text: str, schema_type: str = "invoice") -> ExtractionEnvelope:
        start_time = time.perf_counter()
        schema_type = schema_type.lower()
        target_class: Type[BaseModel] = InvoiceSchema if schema_type == "invoice" else ResumeSchema
        schema_json = json.dumps(target_class.model_json_schema(), indent=2)

        validation_notes: list[str] = []
        prompt = build_extraction_prompt(schema_type, raw_text, schema_json)

        for attempt in range(self.max_retries + 1):
            raw_response, provider_name, is_mock = self.client.generate(prompt)
            sanitized_text = JSONSanitizer.clean(raw_response)

            try:
                parsed_json = json.loads(sanitized_text)
                validated_model = target_class.model_validate(parsed_json)
                latency = round((time.perf_counter() - start_time) * 1000, 2)

                if attempt > 0:
                    validation_notes.append(f"Successfully recovered via self-healing on attempt {attempt + 1}")

                return ExtractionEnvelope(
                    schema_type=schema_type,
                    status="success",
                    provider_used=provider_name,
                    is_mock=is_mock,
                    latency_ms=latency,
                    raw_input_snippet=raw_text[:180] + "..." if len(raw_text) > 180 else raw_text,
                    data=validated_model,
                    validation_notes=validation_notes,
                )

            except (json.JSONDecodeError, ValidationError) as err:
                error_summary = str(err)
                validation_notes.append(f"Attempt {attempt + 1} validation error: {error_summary[:120]}")

                if attempt < self.max_retries:
                    prompt = build_healing_prompt(raw_text, sanitized_text, error_summary, schema_json)
                else:
                    latency = round((time.perf_counter() - start_time) * 1000, 2)
                    return ExtractionEnvelope(
                        schema_type=schema_type,
                        status="validation_failed",
                        provider_used=provider_name,
                        is_mock=is_mock,
                        latency_ms=latency,
                        raw_input_snippet=raw_text[:180] + "...",
                        data={"raw_output": sanitized_text, "error": error_summary},
                        validation_notes=validation_notes,
                    )

        raise ExtractionError("Unexpected exit from extraction loop")
