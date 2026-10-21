"""
Task 1: Structured LLM Prompt Pipeline & JSON Extractor
System instructions, parameterized few-shot templates, and self-healing error prompts.
"""

# ------------------------------------------------------------------------------
# System Instructions
# ------------------------------------------------------------------------------

SYSTEM_INSTRUCTION = """You are a senior data extraction and parsing intelligence engine.
Your sole mission is to ingest messy, unstructured, or OCR-scanned text documents and extract precise,
rigorously typed structured data adhering strictly to the provided JSON Schema.

Rules:
1. Output MUST be a valid single RFC 8259 JSON object.
2. Do NOT enclose your output in markdown code fences (e.g. no ```json or ```).
3. Do NOT include conversational preambles, greetings, or post-extraction explanations.
4. Extract only facts directly stated in or reasonably inferred from the document.
5. If a field is not present in the document and is nullable/optional in the schema, set it to null or empty list.
6. For numeric fields (currency, totals, quantities, tax), ensure values are clean floats/integers without currency symbols.
7. Normalize dates into ISO-8601 YYYY-MM-DD whenever feasible.
"""

# ------------------------------------------------------------------------------
# Few-Shot Exemplars
# ------------------------------------------------------------------------------

FEW_SHOT_INVOICE_INPUT = """
INVOICE #INV-2024-8891
From: Apex Cloud Solutions LLC (Tax ID: US-991823741)
100 Silicon Blvd, Suite 400, San Jose, CA
Contact: billing@apexcloud.io | (408) 555-0199
Billed To: Quantum Dynamics Inc
Attn: Accounts Payable <ap@quantumdyn.com>
Date of Issue: November 14, 2024
Due Date: December 14, 2024
Currency: USD

Items:
- Dedicated Cloud GPU Cluster (A100 x 8) - 1 Month: 1 @ $7,500.00 = $7,500.00
- High-Throughput VPC Peering Gateway: 2 @ $450.00 = $900.00
- 24/7 Enterprise Tier SRE Support: 1 @ $1,200.00 = $1,200.00

Subtotal: $9,600.00
State Sales Tax (8.5%): $816.00
Early Payment Discount: -$200.00
Final Amount Due: $10,216.00
Payment Terms: Net 30
"""

FEW_SHOT_INVOICE_OUTPUT = """{
  "invoice_id": "INV-2024-8891",
  "invoice_date": "2024-11-14",
  "due_date": "2024-12-14",
  "currency": "USD",
  "vendor": {
    "name": "Apex Cloud Solutions LLC",
    "tax_id": "US-991823741",
    "email": "billing@apexcloud.io",
    "phone": "(408) 555-0199",
    "address": "100 Silicon Blvd, Suite 400, San Jose, CA"
  },
  "client": {
    "name": "Quantum Dynamics Inc",
    "email": "ap@quantumdyn.com",
    "phone": null,
    "address": null
  },
  "line_items": [
    {
      "description": "Dedicated Cloud GPU Cluster (A100 x 8) - 1 Month",
      "quantity": 1.0,
      "unit_price": 7500.0,
      "total_price": 7500.0
    },
    {
      "description": "High-Throughput VPC Peering Gateway",
      "quantity": 2.0,
      "unit_price": 450.0,
      "total_price": 900.0
    },
    {
      "description": "24/7 Enterprise Tier SRE Support",
      "quantity": 1.0,
      "unit_price": 1200.0,
      "total_price": 1200.0
    }
  ],
  "subtotal": 9600.0,
  "tax_amount": 816.0,
  "discount_amount": 200.0,
  "total_amount": 10216.0,
  "payment_terms": "Net 30"
}"""

FEW_SHOT_RESUME_INPUT = """
DR. ELENA ROSTOVA
San Francisco, CA | elena.rostova@nexusml.dev | +1 (415) 555-8921
LinkedIn: linkedin.com/in/erostova | GitHub: github.com/erostova

EXECUTIVE SUMMARY
Staff AI & LLM Systems Architect with 8+ years designing scalable agentic workflows, distributed vector databases,
and low-latency inference pipelines. Led multi-agent orchestration projects serving 10M+ daily queries.

WORK EXPERIENCE
Principal AI Engineer — Vanguard Labs (2022 - Present) | San Francisco, CA
- Architected enterprise ReAct agentic framework reducing tool-calling hallucination by 42%.
- Optimized vLLM inference engine on NVIDIA H100 clusters, cutting p99 TTFT latency from 450ms to 110ms.
- Mentored a high-performing squad of 12 machine learning researchers and software engineers.
Technologies: PyTorch, vLLM, LangGraph, Triton, FastAPI, Kubernetes.

Senior Machine Learning Engineer — CognitiveScale (2019 - 2022) | Austin, TX
- Deployed hybrid RAG search combining BM25 dense bi-encoders and Colbert-v2 cross-encoders.
- Authored production ETL pipelines processing 5TB+ daily unstructured text with Ray and Spark.
Technologies: Python, Ray, Spark, ChromaDB, HuggingFace, Docker.

EDUCATION
Ph.D. in Computer Science (Machine Learning Specialization) — Stanford University (2019)
B.S. in Applied Mathematics — UC Berkeley (2014, Summa Cum Laude, GPA 3.96)

TECHNICAL SKILLS
Languages: Python, C++, Rust, SQL, Bash
Frameworks: PyTorch, JAX, HuggingFace, LangChain, FastAPI, Pydantic
Cloud & DevOps: AWS, GCP, Docker, Kubernetes, Terraform, Helm
Databases: PostgreSQL, ChromaDB, Milvus, Redis, Snowflake
"""

FEW_SHOT_RESUME_OUTPUT = """{
  "candidate_name": "Dr. Elena Rostova",
  "email": "elena.rostova@nexusml.dev",
  "phone": "+1 (415) 555-8921",
  "location": "San Francisco, CA",
  "linkedin_url": "https://linkedin.com/in/erostova",
  "github_url": "https://github.com/erostova",
  "professional_summary": "Staff AI & LLM Systems Architect with 8+ years designing scalable agentic workflows, distributed vector databases, and low-latency inference pipelines.",
  "experience": [
    {
      "company": "Vanguard Labs",
      "job_title": "Principal AI Engineer",
      "start_date": "2022-01",
      "end_date": "Present",
      "location": "San Francisco, CA",
      "achievements": [
        "Architected enterprise ReAct agentic framework reducing tool-calling hallucination by 42%.",
        "Optimized vLLM inference engine on NVIDIA H100 clusters, cutting p99 TTFT latency from 450ms to 110ms.",
        "Mentored a high-performing squad of 12 machine learning researchers and software engineers."
      ],
      "skills_used": ["PyTorch", "vLLM", "LangGraph", "Triton", "FastAPI", "Kubernetes"]
    },
    {
      "company": "CognitiveScale",
      "job_title": "Senior Machine Learning Engineer",
      "start_date": "2019-06",
      "end_date": "2022-01",
      "location": "Austin, TX",
      "achievements": [
        "Deployed hybrid RAG search combining BM25 dense bi-encoders and Colbert-v2 cross-encoders.",
        "Authored production ETL pipelines processing 5TB+ daily unstructured text with Ray and Spark."
      ],
      "skills_used": ["Python", "Ray", "Spark", "ChromaDB", "HuggingFace", "Docker"]
    }
  ],
  "education": [
    {
      "institution": "Stanford University",
      "degree": "Ph.D. in Computer Science",
      "field_of_study": "Machine Learning Specialization",
      "graduation_year": 2019,
      "gpa": null
    },
    {
      "institution": "UC Berkeley",
      "degree": "B.S. in Applied Mathematics",
      "field_of_study": null,
      "graduation_year": 2014,
      "gpa": "3.96"
    }
  ],
  "skills": {
    "programming_languages": ["Python", "C++", "Rust", "SQL", "Bash"],
    "frameworks_and_libraries": ["PyTorch", "JAX", "HuggingFace", "LangChain", "FastAPI", "Pydantic"],
    "cloud_and_devops": ["AWS", "GCP", "Docker", "Kubernetes", "Terraform", "Helm"],
    "databases": ["PostgreSQL", "ChromaDB", "Milvus", "Redis", "Snowflake"],
    "tools_and_methods": ["Distributed Systems", "vLLM Optimization", "Cross-Encoder Reranking"]
  },
  "certifications": []
}"""

# ------------------------------------------------------------------------------
# Prompt Builders
# ------------------------------------------------------------------------------

def build_extraction_prompt(schema_type: str, raw_text: str, schema_json: str) -> str:
    """Builds a parameterized few-shot extraction prompt."""
    if schema_type == "invoice":
        few_shot_sample = f"### Exemplar Input:\n{FEW_SHOT_INVOICE_INPUT}\n### Exemplar Output:\n{FEW_SHOT_INVOICE_OUTPUT}\n"
    else:
        few_shot_sample = f"### Exemplar Input:\n{FEW_SHOT_RESUME_INPUT}\n### Exemplar Output:\n{FEW_SHOT_RESUME_OUTPUT}\n"

    return f"""{SYSTEM_INSTRUCTION}

Target JSON Schema:
{schema_json}

{few_shot_sample}
### Current Document to Extract:
\"\"\"
{raw_text}
\"\"\"

Return ONLY the raw JSON object matching the Target JSON Schema above. No extra text or markdown formatting.
"""

def build_healing_prompt(raw_text: str, malformed_json: str, validation_errors: str, schema_json: str) -> str:
    """Builds a targeted correction prompt when Pydantic validation fails."""
    return f"""{SYSTEM_INSTRUCTION}

You previously attempted to extract JSON from the text below, but the output failed strict schema validation.

### Original Document:
\"\"\"
{raw_text}
\"\"\"

### Failed JSON Output:
{malformed_json}

### Validation Errors:
{validation_errors}

### Target JSON Schema:
{schema_json}

Fix the exact errors indicated in the validation log above and output the fully corrected, valid JSON object.
"""
