"""
Task 2: Grounded Document Q&A Assistant (RAG)
FastAPI Web Portal and CLI Query Interface.
Supports document ingestion, similarity search, citations display, and strict abstention.
"""

from __future__ import annotations
import os
import sys
import argparse
from typing import Optional, List
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel

from rag_engine import GroundedRAGEngine, RAGResponse

app = FastAPI(title="ApexAI - Task 2: Grounded Document RAG Assistant", version="1.0.0")

# Singleton RAG engine
rag_engine = GroundedRAGEngine()

# Auto-ingest sample documents on startup if available
SAMPLE_DIR = os.path.join(os.path.dirname(__file__), "samples")
if os.path.exists(SAMPLE_DIR):
    for f in os.listdir(SAMPLE_DIR):
        if f.endswith((".txt", ".md", ".pdf")):
            try:
                rag_engine.ingest_document(os.path.join(SAMPLE_DIR, f))
            except Exception as e:
                print(f"Warning: Failed to auto-ingest {f}: {e}")


class QueryRequest(BaseModel):
    question: str
    top_k: int = 4
    provider: Optional[str] = "mock"


@app.post("/api/query", response_model=RAGResponse)
def api_query(req: QueryRequest):
    """Processes a user question against indexed documents."""
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")
    
    rag_engine.provider = (req.provider or "mock").lower()
    response = rag_engine.answer_question(question=req.question, top_k=req.top_k)
    return response


@app.post("/api/upload")
async def api_upload(file: UploadFile = File(...)):
    """Uploads and indexes a new document into the vector store."""
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in [".pdf", ".txt", ".md"]:
        raise HTTPException(status_code=400, detail="Only PDF, TXT, and MD files are supported.")

    uploads_dir = os.path.join(os.path.dirname(__file__), "uploads")
    os.makedirs(uploads_dir, exist_ok=True)
    save_path = os.path.join(uploads_dir, file.filename)

    content = await file.read()
    with open(save_path, "wb") as f:
        f.write(content)

    num_chunks = rag_engine.ingest_document(save_path)
    return {
        "status": "success",
        "filename": file.filename,
        "chunks_indexed": num_chunks,
        "total_documents": len(rag_engine.indexed_files)
    }


@app.get("/api/status")
def api_status():
    """Returns indexing metrics."""
    return {
        "total_documents": len(rag_engine.indexed_files),
        "indexed_files": rag_engine.indexed_files,
        "total_chunks": len(rag_engine.vector_index.chunks),
        "similarity_threshold": rag_engine.similarity_threshold
    }


@app.get("/", response_class=HTMLResponse)
def index_page():
    return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ApexAI — Task 2: Grounded Document RAG Assistant</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: #090e17;
      --card-bg: #111827;
      --border: #1f2937;
      --accent: #3b82f6;
      --accent-hover: #2563eb;
      --cyan: #06b6d4;
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
    .brand-badge { background: linear-gradient(135deg, #3b82f6, #06b6d4); color: #fff; padding: 6px 12px; border-radius: 8px; font-weight: 700; font-size: 14px; }
    h1 { font-size: 20px; font-weight: 600; }
    .grid { display: grid; grid-template-columns: 380px 1fr; gap: 24px; }
    @media (max-width: 960px) { .grid { grid-template-columns: 1fr; } }
    .card { background: var(--card-bg); border: 1px solid var(--border); border-radius: 12px; padding: 20px; display: flex; flex-direction: column; }
    .card-title { font-size: 16px; font-weight: 600; margin-bottom: 14px; display: flex; justify-content: space-between; align-items: center; }
    .stat-box { background: #0c121e; border: 1px solid var(--border); border-radius: 8px; padding: 12px; margin-bottom: 16px; }
    .stat-row { display: flex; justify-content: space-between; font-size: 13px; margin-bottom: 6px; }
    .stat-row strong { color: var(--cyan); }
    .file-list { max-height: 140px; overflow-y: auto; list-style: none; font-size: 12.5px; color: var(--text-muted); font-family: var(--mono); }
    .file-list li { padding: 4px 0; border-bottom: 1px solid rgba(255,255,255,0.05); }
    .suggested-box { margin-top: 16px; }
    .suggest-btn { display: block; width: 100%; text-align: left; padding: 8px 10px; margin-bottom: 8px; background: rgba(59, 130, 246, 0.08); border: 1px solid rgba(59, 130, 246, 0.2); color: #bfdbfe; border-radius: 6px; font-size: 12.5px; cursor: pointer; transition: all 0.15s ease; }
    .suggest-btn:hover { background: rgba(59, 130, 246, 0.2); border-color: var(--accent); }
    .query-bar { display: flex; gap: 10px; margin-bottom: 20px; }
    input[type="text"] { flex: 1; padding: 12px 16px; border-radius: 8px; border: 1px solid var(--border); background: #0c121e; color: var(--text); font-size: 14px; outline: none; }
    input[type="text"]:focus { border-color: var(--accent); }
    button { padding: 10px 20px; border-radius: 8px; border: none; cursor: pointer; font-weight: 600; font-size: 14px; transition: all 0.15s ease; }
    button.primary { background: var(--accent); color: #fff; }
    button.primary:hover { background: var(--accent-hover); }
    .answer-box { background: #0c121e; border: 1px solid var(--border); border-radius: 8px; padding: 20px; margin-bottom: 20px; min-height: 120px; }
    .answer-text { font-size: 15px; line-height: 1.6; color: #e5e7eb; margin-bottom: 14px; }
    .citations-container { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 12px; }
    .citation-chip { background: rgba(6, 182, 212, 0.12); border: 1px solid rgba(6, 182, 212, 0.3); color: var(--cyan); padding: 4px 10px; border-radius: 6px; font-size: 12px; font-family: var(--mono); }
    .abstention-chip { background: rgba(239, 68, 68, 0.12); border: 1px solid rgba(239, 68, 68, 0.3); color: var(--danger); padding: 4px 10px; border-radius: 6px; font-size: 12px; }
    .chunks-section { border-top: 1px solid var(--border); padding-top: 16px; }
    .chunk-card { background: #131b2c; border: 1px solid rgba(255,255,255,0.06); border-radius: 6px; padding: 12px; margin-bottom: 10px; font-size: 13px; font-family: var(--mono); line-height: 1.5; color: #cbd5e1; }
    .chunk-meta { display: flex; justify-content: space-between; font-size: 11.5px; color: var(--text-muted); margin-bottom: 6px; border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 4px; }
  </style>
</head>
<body>
  <div class="container">
    <header>
      <div class="brand">
        <span class="brand-badge">ApexAI</span>
        <div>
          <h1>Task 2: Grounded Document Q&A Assistant (RAG)</h1>
          <p style="font-size: 13px; color: var(--text-muted);">Vector Embeddings, Semantic Chunking, Page Citations & Hallucination Abstention</p>
        </div>
      </div>
      <div>
        <span style="font-size: 12px; padding: 4px 10px; border-radius: 999px; background: rgba(59, 130, 246, 0.15); color: #60a5fa; border: 1px solid rgba(59, 130, 246, 0.3);">RAG Pipeline Active</span>
      </div>
    </header>

    <div class="grid">
      <!-- Left: Corpus & Upload -->
      <div class="card">
        <div class="card-title">Document Corpus Status</div>
        <div class="stat-box" id="statBox">
          <div class="stat-row"><span>Indexed Documents:</span> <strong id="docCount">0</strong></div>
          <div class="stat-row"><span>Total Vector Chunks:</span> <strong id="chunkCount">0</strong></div>
          <div class="stat-row"><span>Similarity Threshold:</span> <strong id="thresholdVal">0.20</strong></div>
        </div>

        <div style="font-size: 12px; font-weight: 600; text-transform: uppercase; margin-bottom: 8px; color: var(--text-muted);">Loaded Documents:</div>
        <ul class="file-list" id="fileList">
          <li>Loading corpus files...</li>
        </ul>

        <div class="suggested-box">
          <div style="font-size: 12px; font-weight: 600; text-transform: uppercase; margin-bottom: 8px; color: var(--text-muted);">Test Questions:</div>
          <button class="suggest-btn" onclick="askPreset('What is the maximum daily meal reimbursement limit for domestic travel?')">🍽️ Meal allowance limit?</button>
          <button class="suggest-btn" onclick="askPreset('When is an employee permitted to book business class airfare?')">✈️ Business class policy?</button>
          <button class="suggest-btn" onclick="askPreset('What are the Recovery Point Objective (RPO) and encryption standards for cloud databases?')">🔐 Cloud encryption & RPO?</button>
          <button class="suggest-btn" onclick="askPreset('What is the corporate reimbursement policy for commercial rocket flights to Mars?')">🚀 Mars Rocket (Abstention Test)</button>
        </div>
      </div>

      <!-- Right: Q&A Interface -->
      <div class="card">
        <div class="card-title">Interactive Grounded Q&A</div>
        <div class="query-bar">
          <input type="text" id="queryInput" placeholder="Ask a question about the uploaded policies and technical architecture..." onkeydown="if(event.key==='Enter') runQuery()">
          <button class="primary" id="queryBtn" onclick="runQuery()">Ask Assistant</button>
        </div>

        <div class="answer-box">
          <div class="answer-text" id="answerDisplay">Ask a question above or click one of the suggested prompts to test the RAG engine...</div>
          <div class="citations-container" id="citationsDisplay"></div>
        </div>

        <div class="chunks-section">
          <div class="card-title" style="font-size: 14px; margin-bottom: 10px;">Retrieved Source Chunks & Relevance Scores</div>
          <div id="chunksDisplay" style="color: var(--text-muted); font-size: 13px;">No chunks retrieved yet.</div>
        </div>
      </div>
    </div>
  </div>

  <script>
    window.onload = loadCorpusStatus;

    async function loadCorpusStatus() {
      try {
        const res = await fetch('/api/status');
        const data = await res.json();
        document.getElementById('docCount').textContent = data.total_documents;
        document.getElementById('chunkCount').textContent = data.total_chunks;
        document.getElementById('thresholdVal').textContent = data.similarity_threshold;

        const list = document.getElementById('fileList');
        list.innerHTML = '';
        data.indexed_files.forEach(f => {
          const li = document.createElement('li');
          li.textContent = '📄 ' + f;
          list.appendChild(li);
        });
      } catch (err) {
        console.error('Failed to load status:', err);
      }
    }

    function askPreset(q) {
      document.getElementById('queryInput').value = q;
      runQuery();
    }

    async function runQuery() {
      const q = document.getElementById('queryInput').value.trim();
      if (!q) return;

      const btn = document.getElementById('queryBtn');
      btn.disabled = true;
      btn.textContent = 'Searching...';
      document.getElementById('answerDisplay').textContent = 'Retrieving vector chunks and synthesizing grounded answer...';
      document.getElementById('citationsDisplay').innerHTML = '';

      try {
        const res = await fetch('/api/query', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ question: q, top_k: 4, provider: 'mock' })
        });
        const data = await res.json();

        document.getElementById('answerDisplay').textContent = data.answer;
        const citContainer = document.getElementById('citationsDisplay');
        citContainer.innerHTML = '';

        if (data.is_abstention) {
          const chip = document.createElement('span');
          chip.className = 'abstention-chip';
          chip.textContent = '🛡️ Strict Abstention Triggered (No Hallucination)';
          citContainer.appendChild(chip);
        } else {
          data.citations.forEach(c => {
            const chip = document.createElement('span');
            chip.className = 'citation-chip';
            chip.textContent = `📍 ${c.source_file} (Page ${c.page_number}, Score: ${c.relevance_score})`;
            citContainer.appendChild(chip);
          });
        }

        const chunksContainer = document.getElementById('chunksDisplay');
        chunksContainer.innerHTML = '';
        if (data.retrieved_chunks.length === 0) {
          chunksContainer.textContent = 'No document chunks exceeded the relevance threshold.';
        } else {
          data.retrieved_chunks.forEach(r => {
            const card = document.createElement('div');
            card.className = 'chunk-card';
            card.innerHTML = `
              <div class="chunk-meta">
                <span>Rank #${r.rank} • ${r.chunk.source_file} (Page ${r.chunk.page_number})</span>
                <span style="color: var(--cyan);">Cosine Similarity: ${r.similarity_score}</span>
              </div>
              <div>${r.chunk.text}</div>
            `;
            chunksContainer.appendChild(card);
          });
        }
      } catch (err) {
        document.getElementById('answerDisplay').textContent = 'Error: ' + err.message;
      } finally {
        btn.disabled = false;
        btn.textContent = 'Ask Assistant';
      }
    }
  </script>
</body>
</html>"""


def run_cli():
    parser = argparse.ArgumentParser(description="ApexAI Task 2: Grounded Document RAG CLI")
    parser.add_argument("--query", "-q", help="User question to answer against corpus")
    parser.add_argument("--file", "-f", help="Ingest a specific document before querying")
    parser.add_argument("--provider", "-p", default="mock", help="Provider: 'mock', 'gemini', 'openai'")
    parser.add_argument("--serve", action="store_true", help="Launch FastAPI web portal on port 8002")
    args = parser.parse_args()

    if args.serve or len(sys.argv) == 1:
        import uvicorn
        port = int(os.getenv("TASK2_PORT", "8002"))
        print(f"Starting ApexAI Task 2 RAG Portal on http://127.0.0.1:{port}")
        uvicorn.run("app:app", host="127.0.0.1", port=port, reload=False)
        return

    if args.file and os.path.exists(args.file):
        rag_engine.ingest_document(args.file)

    if not args.query:
        print("Error: Specify a question with --query or launch web portal with --serve")
        sys.exit(1)

    rag_engine.provider = args.provider
    response = rag_engine.answer_question(args.query)

    print("\n" + "=" * 65)
    print(f"QUESTION: {response.question}")
    print("=" * 65)
    print(f"ANSWER: {response.answer}\n")
    if response.is_abstention:
        print("STATUS: Strict Abstention Triggered (Information not present in corpus)")
    else:
        print("CITATIONS:")
        for c in response.citations:
            print(f" - {c.source_file} (Page {c.page_number}, Score: {c.relevance_score})")
    print("=" * 65)


if __name__ == "__main__":
    run_cli()
