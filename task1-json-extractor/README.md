# Task 1: Structured LLM Prompt Pipeline & JSON Extractor
## ApexAI Engineering Operations Suite

A production-grade information extraction engine that ingests unstructured, noisy, or OCR-scanned text documents (such as financial invoices and candidate resumes) and extracts strictly validated JSON matching Pydantic v2 schemas.

---

## 🚀 Key Features

1. **Pydantic v2 Strict Validation**:
   - `InvoiceSchema`: Vendor details, client details, line items with positive unit prices and quantities, automated arithmetic checks enforcing `subtotal + tax - discount == total_amount`.
   - `ResumeSchema`: Normalized candidate name, email validation, structured work histories, categorized technical skills, and educational records.
2. **Multi-Pass JSON Sanitizer**:
   - Strips markdown code blocks (````json ... ````).
   - Extracts balanced JSON substrings between outer brackets `{ ... }`.
   - Heals common trailing commas and removes conversational preambles/postambles.
3. **Self-Healing Error Recovery**:
   - If validation errors occur, feeds detailed Pydantic error traces back into the model to fix exact faulty fields without re-extracting unchanged data.
4. **Dual Provider & Deterministic Offline Mock**:
   - Seamlessly uses **Google Gemini 1.5** or **OpenAI GPT-4o-mini** when API keys are configured.
   - Includes a deterministic, keyword-aware **Offline Mock Engine** so evaluators can run the system and test suites with zero external API dependencies.
5. **Interactive FastAPI UI & CLI**:
   - Browser portal on port 8001 with sample text loader, real-time latency monitoring, and one-click JSON download.
   - Comprehensive CLI runner for headless batch processing.

---

## 📁 Directory Structure

```text
task1-json-extractor/
├── app.py                   # FastAPI web portal & CLI runner
├── extractor.py             # StructuredJSONExtractor & LLM Client
├── sanitizer.py             # Multi-pass JSON healing pre-parser
├── schemas.py               # ExtractionEnvelope & unified schema exports
├── invoice_schema.py        # Pydantic v2 Invoice models & validators
├── resume_schema.py         # Pydantic v2 Resume models & validators
├── prompts.py               # Parameterized prompts & few-shot exemplars
├── requirements.txt         # Standalone task dependencies
├── README.md                # Task documentation
├── samples/                 # Realistic test documents
│   ├── invoice_standard.txt
│   ├── invoice_noisy_ocr.txt
│   ├── resume_senior_architect.txt
│   └── resume_data_engineer.txt
└── tests/                   # Pytest automated test suite
    ├── __init__.py
    ├── test_schemas.py
    └── test_extractor.py
```

---

## 🛠️ Usage Instructions

### 1. Web Portal Mode (Interactive UI)
Start the FastAPI server:
```bash
python task1-json-extractor/app.py --serve
```
Open your browser at **`http://127.0.0.1:8001`**.
- Choose between Invoice and Resume schemas.
- Select a realistic sample from the dropdown or paste your own document text.
- Select provider (Mock, Gemini, or OpenAI) and click **Extract & Validate JSON**.
- Click **Download JSON** to export the structured payload.

### 2. CLI Mode (Headless Batch)
Extract structured data from an input file:
```bash
python task1-json-extractor/app.py --file task1-json-extractor/samples/invoice_standard.txt --type invoice --output invoice_output.json
```

Extract a candidate resume:
```bash
python task1-json-extractor/app.py --file task1-json-extractor/samples/resume_senior_architect.txt --type resume
```

---

## 🧪 Running Automated Tests

Run the dedicated test suite:
```bash
pytest task1-json-extractor/tests -v
```
Expected output: 11 passing tests verifying schema constraints, currency normalization, line-item arithmetic, markdown fence stripping, and mock extraction.
