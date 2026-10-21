# Task 2: Grounded Document Q&A Assistant with RAG & Vector Embeddings
## Person 1 Implementation — ApexAI Suite

A vector-augmented retrieval-augmented generation (RAG) system capable of ingesting PDF and plaintext documents, chunking text recursively with metadata preservation, performing cosine similarity search, and generating grounded responses with explicit source-page citations and strict hallucination abstention.

---

## 🚀 Key Features

1. **Page-Aware Ingestion Engine**:
   - Parses multi-page `.pdf` files via `pypdf` alongside `.txt` and `.md` files.
   - Preserves originating filename, 1-indexed page number, and character length for every page.
2. **Recursive Character Semantic Chunker**:
   - Hierarchically splits documents using separators (`\n\n` -> `\n` -> `. ` -> ` `).
   - Configurable chunk size (default: 600 chars) and overlap (default: 120 chars) to maintain conversational context across chunk boundaries.
3. **Dual Vector Store & Resilient Cosine Index**:
   - High-performance, zero-external-dependency vector embedding engine using subword n-gram TF-IDF and cosine similarity.
   - Guaranteed 100% platform portability across Windows, macOS, and Linux without native C++ compilation overhead.
4. **Strict Hallucination Abstention**:
   - Enforces a similarity threshold gate (default: 0.20).
   - If the corpus lacks relevant factual evidence, the engine strictly outputs:
     `"I cannot find sufficient evidence in the provided documents to answer this question."`
5. **Granular Source Citations**:
   - Every claim is backed by explicit citations formatted as:
     `[Source: <filename>, Page: <page_number>, Score: <cosine_similarity>]`.
6. **FastAPI Web Portal & Interactive CLI**:
   - Browser portal on port 8002 featuring document upload, corpus statistics, and interactive Q&A.
   - Headless CLI runner for single-query retrieval and scripting.

---

## 📁 Directory Structure

```text
task2-document-rag/
├── app.py                   # FastAPI web portal & CLI query engine
├── ingestion.py             # Document loader for PDF, TXT, MD
├── chunker.py               # RecursiveCharacterChunker module
├── retrieval.py             # ResilientCosineVectorIndex & SearchResult
├── rag_engine.py            # GroundedRAGEngine with citations & abstention
├── requirements.txt         # Standalone dependencies
├── README.md                # Task 2 documentation
├── samples/                 # Sample policy and technical whitepaper
│   ├── employee_travel_policy.txt
│   └── cloud_architecture_security.txt
└── tests/                   # Pytest automated test suite
    ├── __init__.py
    └── test_rag.py
```

---

## 🛠️ Usage Instructions

### 1. Web Portal Mode (Interactive UI)
Start the FastAPI server:
```bash
python task2-document-rag/app.py --serve
```
Open **`http://127.0.0.1:8002`** in your browser.
- View currently indexed documents in the corpus.
- Click any of the preloaded suggested questions or enter your own query.
- Review the grounded answer, citation chips, and raw matching text chunks.
- Test strict abstention by asking about topics not covered in the documents (e.g. *"What is the policy on rocket flights to Mars?"*).

### 2. CLI Mode (Headless Query)
Run a direct question from the terminal:
```bash
python task2-document-rag/app.py --query "What is the daily meal per diem allowance?"
```

Ingest an external document and query it immediately:
```bash
python task2-document-rag/app.py --file path/to/document.pdf --query "Summarize the encryption policy"
```

---

## 🧪 Running Automated Tests

Execute the automated test suite:
```bash
pytest task2-document-rag/tests -v
```
Expected output: 5 passing tests validating PDF/text ingestion, chunk boundary overlap, vector ranking accuracy, citation attribution, and strict abstention behavior.
