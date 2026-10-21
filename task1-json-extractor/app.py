"""
Task 1: Structured LLM Prompt Pipeline & JSON Extractor
Full-featured Web Application (FastAPI) and CLI interface.
Supports live interactive extraction, sample loading, schema validation, and JSON download.
"""

from __future__ import annotations
import os
import sys
import json
import argparse
from typing import Optional
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel

from extractor import StructuredJSONExtractor
from schemas import ExtractionEnvelope

app = FastAPI(title="ApexAI - Task 1: Structured JSON Extractor", version="1.0.0")

# Preloaded realistic samples
SAMPLE_INVOICE_STANDARD = """INVOICE #INV-2025-0442
Vendor: Apex Cloud Infrastructure LLC
Tax ID: US-449182371 | Email: accounts@apexcloud.io | Phone: +1 (415) 555-0912
Address: 500 Howard Street, Suite 300, San Francisco, CA 94105

Billed To: HyperScale Intelligence Inc
Contact: finance@hyperscale.ai | Phone: +1 (650) 555-7721
Address: 1200 Innovation Way, Palo Alto, CA 94301

Date Issued: 2025-02-15
Payment Due: 2025-03-15
Currency: USD
Payment Terms: Net 30

Line Items:
1. High-Performance GPU Cluster (8x NVIDIA H100 SXM5) - Monthly Lease
   Qty: 1.0 | Unit Price: $14,500.00 | Total: $14,500.00
2. Dedicated 100 Gbps Low-Latency Interconnect Gateway
   Qty: 2.0 | Unit Price: $850.00 | Total: $1,700.00
3. Distributed Object Storage (200 TB High-IOPS Tier)
   Qty: 1.0 | Unit Price: $3,200.00 | Total: $3,200.00

Subtotal: $19,400.00
Sales Tax (8.25%): $1,600.50
Early Payment Discount: -$400.00
Total Amount Due: $20,600.50"""

SAMPLE_INVOICE_NOISY = """*** SCANNED OCR BILLING NOTICE ***
APEX CLOUD SYSTEMS [TAX_ID: US-449182371]
support billing: accounts@apexcloud.io
INV REF: INV-2025-9981 --- DTD: 2025-01-10
CUSTOMER: Datacore Analytics LLC (billing@datacore.net)
100 Park Ave NY
CURR: US DOLLARS
-- SERVICES --
* Cloud Managed Vector DB Shards (3 nodes): 3 qty @ 600.00 ea => 1800.00
* Automated Backup & Snapshotting: 1 @ 250.00 => 250.00
sub-total is 2050.00
applicable state tax 164.00
discount: 0.0
TOTAL PAYABLE: 2214.00
Please remit payment within 15 days."""

SAMPLE_RESUME = """DR. ARJUN RAMAN
Seattle, WA | arjun.raman@apexai.dev | +1 (206) 555-0144
LinkedIn: linkedin.com/in/arjunraman | GitHub: github.com/arjunraman

PROFESSIONAL SUMMARY
Senior Distributed AI Systems Engineer with 8+ years architecting fault-tolerant LLM pipelines,
agentic execution environments, and sub-10ms vector search backends. Published researcher in scalable AI inference.

EXPERIENCE
Staff AI Infrastructure Engineer | Apex Systems (2022 - Present) | Seattle, WA
- Designed high-throughput vector embedding retrieval microservice serving 40k QPS across 4 regions.
- Implemented ReAct agent governance architecture eliminating unsafe shell executions and arbitrary tool calls.
- Reduced inference infrastructure costs by 38% via INT8/FP8 dynamic quantization.
Technologies: Python, PyTorch, vLLM, FastAPI, Kubernetes, Docker, Ray, Triton.

Senior Machine Learning Engineer | DeepFlow Data (2018 - 2022) | Austin, TX
- Built automated document ingestion and structured metadata extraction engine processing 1M+ daily records.
- Implemented recursive semantic chunking and cross-encoder reranking algorithms.
Technologies: Python, Spark, HuggingFace, ChromaDB, AWS, PostgreSQL.

EDUCATION
Ph.D. in Computer Science (Artificial Intelligence) | University of Washington (2018)
B.S. in Electrical Engineering & Computer Science | UC Berkeley (2014, GPA: 3.94)

CORE COMPETENCIES
Languages: Python, C++, Go, Rust, SQL, Bash
Frameworks: PyTorch, LangChain, FastAPI, Pydantic, Streamlit, Docker
Cloud: AWS, Google Cloud Platform, Terraform, Kubernetes, Prometheus
Databases: PostgreSQL, ChromaDB, Redis, Milvus"""


class ExtractionRequest(BaseModel):
    raw_text: str
    schema_type: str = "invoice"
    provider: Optional[str] = "mock"


@app.post("/api/extract", response_model=ExtractionEnvelope)
def api_extract(req: ExtractionRequest):
    """API endpoint to perform structured extraction."""
    if not req.raw_text.strip():
        raise HTTPException(status_code=400, detail="Document text cannot be empty.")
    
    extractor = StructuredJSONExtractor(provider=req.provider)
    result = extractor.extract(raw_text=req.raw_text, schema_type=req.schema_type)
    return result


@app.get("/api/samples/{sample_id}")
def api_get_sample(sample_id: str):
    """Returns sample text documents."""
    samples = {
        "invoice_standard": {"text": SAMPLE_INVOICE_STANDARD, "type": "invoice"},
        "invoice_noisy": {"text": SAMPLE_INVOICE_NOISY, "type": "invoice"},
        "resume_standard": {"text": SAMPLE_RESUME, "type": "resume"},
    }
    if sample_id not in samples:
        raise HTTPException(status_code=404, detail="Sample not found.")
    return samples[sample_id]


@app.get("/", response_class=HTMLResponse)
def index_page():
    """Serves the standalone browser interface for Task 1."""
    return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ApexAI — Task 1: Structured LLM JSON Extractor</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: #0b0f19;
      --card-bg: #111827;
      --border: #1f2937;
      --accent: #06b6d4;
      --accent-hover: #0891b2;
      --text: #f3f4f6;
      --text-muted: #9ca3af;
      --success: #10b981;
      --warn: #f59e0b;
      --danger: #ef4444;
      --font: 'Inter', -apple-system, sans-serif;
      --mono: 'JetBrains Mono', monospace;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { background: var(--bg); color: var(--text); font-family: var(--font); line-height: 1.5; padding: 24px; min-height: 100vh; }
    .container { max-width: 1400px; margin: 0 auto; }
    header { display: flex; justify-content: space-between; align-items: center; padding-bottom: 20px; border-bottom: 1px solid var(--border); margin-bottom: 24px; }
    .brand { display: flex; align-items: center; gap: 12px; }
    .brand-badge { background: linear-gradient(135deg, #06b6d4, #3b82f6); color: #fff; padding: 6px 12px; border-radius: 8px; font-weight: 700; font-size: 14px; letter-spacing: 0.5px; }
    h1 { font-size: 20px; font-weight: 600; }
    .badge-status { font-size: 12px; padding: 4px 10px; border-radius: 999px; background: rgba(16, 185, 129, 0.15); color: var(--success); border: 1px solid rgba(16, 185, 129, 0.3); font-weight: 500; }
    .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }
    @media (max-width: 960px) { .grid { grid-template-columns: 1fr; } }
    .card { background: var(--card-bg); border: 1px solid var(--border); border-radius: 12px; padding: 20px; display: flex; flex-direction: column; }
    .card-title { font-size: 16px; font-weight: 600; margin-bottom: 16px; display: flex; justify-content: space-between; align-items: center; }
    .toolbar { display: flex; gap: 10px; margin-bottom: 12px; flex-wrap: wrap; }
    select, button, textarea { font-family: var(--font); border-radius: 6px; border: 1px solid var(--border); background: #1a2234; color: var(--text); font-size: 14px; }
    select { padding: 8px 12px; cursor: pointer; outline: none; }
    button { padding: 8px 16px; cursor: pointer; font-weight: 500; transition: all 0.15s ease; }
    button.primary { background: var(--accent); color: #000; border-color: var(--accent); font-weight: 600; }
    button.primary:hover { background: var(--accent-hover); }
    button.secondary { background: #1f2937; color: var(--text); }
    button.secondary:hover { background: #374151; }
    textarea { width: 100%; height: 420px; padding: 14px; font-family: var(--mono); font-size: 13px; line-height: 1.6; resize: vertical; outline: none; background: #0e1422; }
    textarea:focus { border-color: var(--accent); }
    .output-viewer { width: 100%; height: 420px; background: #0e1422; border: 1px solid var(--border); border-radius: 6px; padding: 14px; font-family: var(--mono); font-size: 12.5px; overflow: auto; white-space: pre-wrap; word-break: break-all; color: #a5f3fc; }
    .meta-bar { margin-top: 14px; padding: 12px; background: #151d30; border-radius: 8px; font-size: 13px; display: flex; gap: 20px; flex-wrap: wrap; color: var(--text-muted); }
    .meta-item strong { color: var(--text); }
    .loading-spinner { display: none; margin-left: 8px; animation: spin 1s linear infinite; }
    @keyframes spin { 100% { transform: rotate(360deg); } }
  </style>
</head>
<body>
  <div class="container">
    <header>
      <div class="brand">
        <span class="brand-badge">ApexAI</span>
        <div>
          <h1>Task 1: Structured LLM Prompt Pipeline & JSON Extractor</h1>
          <p style="font-size: 13px; color: var(--text-muted);">Pydantic v2 Strict Schema Validation & Self-Healing Extraction Pipeline</p>
        </div>
      </div>
      <div>
        <span class="badge-status">API Ready (Live / Mock)</span>
      </div>
    </header>

    <div class="grid">
      <!-- Input Card -->
      <div class="card">
        <div class="card-title">
          <span>Unstructured Document Input</span>
          <span style="font-size: 12px; color: var(--text-muted);">Raw text / OCR dump</span>
        </div>

        <div class="toolbar">
          <select id="schemaType" onchange="onSchemaChange()">
            <option value="invoice">Schema: Invoice (Financial)</option>
            <option value="resume">Schema: Resume (Professional)</option>
          </select>

          <select id="sampleLoader" onchange="loadSelectedSample()">
            <option value="">-- Load Realistic Sample --</option>
            <option value="invoice_standard">Standard Cloud Invoice (Clean)</option>
            <option value="invoice_noisy">Noisy OCR Scanned Bill</option>
            <option value="resume_standard">Staff Systems Architect Resume</option>
          </select>

          <select id="providerSelect">
            <option value="mock">Provider: Offline Mock Engine (Deterministic)</option>
            <option value="gemini">Provider: Google Gemini 1.5</option>
            <option value="openai">Provider: OpenAI GPT-4o-mini</option>
          </select>
        </div>

        <textarea id="rawInput" placeholder="Paste unstructured invoice or resume text here, or choose a sample from the dropdown..."></textarea>

        <div style="margin-top: 14px; display: flex; gap: 10px;">
          <button class="primary" id="extractBtn" onclick="runExtraction()">
            <span>Extract & Validate JSON</span>
            <span class="loading-spinner" id="spinner">⏳</span>
          </button>
          <button class="secondary" onclick="clearInput()">Clear</button>
        </div>
      </div>

      <!-- Output Card -->
      <div class="card">
        <div class="card-title">
          <span>Validated Pydantic v2 JSON Output</span>
          <button class="secondary" id="downloadBtn" onclick="downloadJSON()" style="padding: 4px 12px; font-size: 12px;" disabled>Download JSON</button>
        </div>

        <div class="output-viewer" id="outputJson">// Validated JSON will render here after extraction...</div>

        <div class="meta-bar" id="metaBar">
          <div class="meta-item">Status: <strong id="metaStatus">Ready</strong></div>
          <div class="meta-item">Provider: <strong id="metaProvider">None</strong></div>
          <div class="meta-item">Latency: <strong id="metaLatency">0 ms</strong></div>
          <div class="meta-item">Schema: <strong id="metaSchema">invoice</strong></div>
        </div>
      </div>
    </div>
  </div>

  <script>
    let currentResult = null;

    // Load initial sample
    window.onload = () => {
      document.getElementById('sampleLoader').value = 'invoice_standard';
      loadSelectedSample();
    };

    function onSchemaChange() {
      const type = document.getElementById('schemaType').value;
      const loader = document.getElementById('sampleLoader');
      if (type === 'resume') {
        loader.value = 'resume_standard';
      } else {
        loader.value = 'invoice_standard';
      }
      loadSelectedSample();
    }

    async function loadSelectedSample() {
      const sampleId = document.getElementById('sampleLoader').value;
      if (!sampleId) return;
      try {
        const res = await fetch(`/api/samples/${sampleId}`);
        const data = await res.json();
        document.getElementById('rawInput').value = data.text;
        document.getElementById('schemaType').value = data.type;
      } catch (err) {
        console.error("Failed to load sample:", err);
      }
    }

    function clearInput() {
      document.getElementById('rawInput').value = '';
      document.getElementById('outputJson').textContent = '// Ready for new input...';
      document.getElementById('downloadBtn').disabled = true;
    }

    async function runExtraction() {
      const rawText = document.getElementById('rawInput').value.trim();
      if (!rawText) {
        alert("Please paste document text or load a sample first.");
        return;
      }

      const schemaType = document.getElementById('schemaType').value;
      const provider = document.getElementById('providerSelect').value;
      const btn = document.getElementById('extractBtn');
      const spinner = document.getElementById('spinner');

      btn.disabled = true;
      spinner.style.display = 'inline-block';
      document.getElementById('outputJson').textContent = 'Processing extraction with Pydantic v2 validation...';

      try {
        const response = await fetch('/api/extract', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ raw_text: rawText, schema_type: schemaType, provider: provider })
        });

        const envelope = await response.json();
        currentResult = envelope;

        document.getElementById('outputJson').textContent = JSON.stringify(envelope.data, null, 2);
        document.getElementById('metaStatus').textContent = envelope.status.toUpperCase();
        document.getElementById('metaStatus').style.color = envelope.status === 'success' ? '#10b981' : '#f59e0b';
        document.getElementById('metaProvider').textContent = envelope.provider_used + (envelope.is_mock ? ' (Mock)' : ' (Live)');
        document.getElementById('metaLatency').textContent = envelope.latency_ms + ' ms';
        document.getElementById('metaSchema').textContent = envelope.schema_type;
        document.getElementById('downloadBtn').disabled = false;

      } catch (err) {
        document.getElementById('outputJson').textContent = 'Error: ' + err.message;
        document.getElementById('metaStatus').textContent = 'ERROR';
        document.getElementById('metaStatus').style.color = '#ef4444';
      } finally {
        btn.disabled = false;
        spinner.style.display = 'none';
      }
    }

    function downloadJSON() {
      if (!currentResult || !currentResult.data) return;
      const blob = new Blob([JSON.stringify(currentResult.data, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `extracted_${currentResult.schema_type}_${Date.now()}.json`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    }
  </script>
</body>
</html>"""


def run_cli():
    """Runs extraction via command-line."""
    parser = argparse.ArgumentParser(description="ApexAI Task 1: Structured JSON Extractor CLI")
    parser.add_argument("--file", "-f", help="Path to input text document", required=False)
    parser.add_argument("--type", "-t", choices=["invoice", "resume"], default="invoice", help="Extraction schema type")
    parser.add_argument("--provider", "-p", default="mock", help="Provider: 'mock', 'gemini', 'openai'")
    parser.add_argument("--output", "-o", help="Optional output JSON filepath", required=False)
    parser.add_argument("--serve", action="store_true", help="Launch FastAPI web server on port 8001")
    args = parser.parse_args()

    if args.serve or len(sys.argv) == 1:
        import uvicorn
        port = int(os.getenv("TASK1_PORT", "8001"))
        print(f"Starting ApexAI Task 1 Web Portal on http://127.0.0.1:{port}")
        uvicorn.run("app:app", host="127.0.0.1", port=port, reload=False)
        return

    if not args.file:
        print("Error: Specify an input file with --file or start web server with --serve")
        sys.exit(1)

    if not os.path.exists(args.file):
        print(f"Error: File '{args.file}' not found.")
        sys.exit(1)

    with open(args.file, "r", encoding="utf-8") as f:
        text = f.read()

    extractor = StructuredJSONExtractor(provider=args.provider)
    result = extractor.extract(raw_text=text, schema_type=args.type)

    formatted_json = json.dumps(result.model_dump(), indent=2)
    print("\n" + "=" * 60)
    print(f"EXTRACTION RESULT [{result.status.upper()}] (Provider: {result.provider_used})")
    print("=" * 60)
    print(formatted_json)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as out_f:
            out_f.write(formatted_json)
        print(f"\nSaved structured result to: {args.output}")


if __name__ == "__main__":
    run_cli()
