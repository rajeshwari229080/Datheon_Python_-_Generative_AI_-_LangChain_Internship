# System Architecture & Technical Specifications
## ApexAI Engineering Operations Suite

This document outlines the architectural blueprints, subsystem boundaries, data flow pipelines, and security guardrails governing the ApexAI Suite.

---

## 🏛️ End-to-End System Architecture

```text
                               +----------------------------+
                               | Central Operations Portal  |
                               |        index.html          |
                               +--------------+-------------+
                                              |
                +-----------------------------+-----------------------------+
                |                             |                             |
                v                             v                             v
+-------------------------------+  +--------------------+  +--------------------------------+
|  Task 1: Structured Extractor |  |  Task 2: RAG Q&A   |  |   Task 3: Autonomous Agent     |
|  - Pydantic v2 Validation     |  |  - pypdf Ingestion |  |   - ReAct Reasoning Loop       |
|  - Multi-Pass JSON Sanitizer  |  |  - Chunker (600/120|  |   - AST Math Calculator        |
|  - Self-Healing Retry Loop    |  |  - Cosine Vectors  |  |   - Jailed Safe File Reader    |
|  - Dual Provider + Mock       |  |  - Page Citations  |  |   - DuckDuckGo Web Search      |
+---------------+---------------+  +---------+----------+  +---------------+----------------+
                |                            |                             |
                +----------------------------+-----------------------------+
                                             |
                                             v
                              +------------------------------+
                              |   Task 4: Streamlit Chatbot  |
                              |   - Reactive Chat UI         |
                              |   - Persona System Prompts   |
                              |   - Token Streaming          |
                              |   - Session Isolation        |
                              +------------------------------+
```

---

## 🧩 Subsystem Specifications

### Task 1: Structured LLM Prompt Pipeline & JSON Extractor
- **Validation Engine**: Pydantic v2 (`model_validate`, `model_json_schema`).
- **Data Schemas**:
  - `InvoiceSchema`: Vendor and client details, validated line items with positive unit prices and quantities, automated arithmetic checks enforcing subtotal and total consistency.
  - `ResumeSchema`: Candidate identity, email validation, structured work histories, categorized technical skills, and educational records.
- **Error Recovery**: Multi-pass sanitizer extracts balanced JSON, strips markdown code blocks, and cleans trailing commas. In case of schema violation, sends targeted error feedback to the model for self-healing repair.

### Task 2: Grounded Document Q&A Assistant (RAG)
- **Ingestion Pipeline**: Multi-page PDF text extraction via `pypdf`, preserving originating document name and 1-indexed page numbers.
- **Recursive Character Chunker**: Splits text using a hierarchy of separators (`\n\n`, `\n`, `. `, ` `) with 600-character chunk sizes and 120-character overlaps.
- **Vector Retrieval**: Pure-Python / numpy subword n-gram TF-IDF and cosine similarity index (`ResilientCosineVectorIndex`), providing zero-compilation cross-platform portability.
- **Hallucination Prevention**: Strict abstention threshold (default: 0.20). If factual evidence is absent, returns:
  `"I cannot find sufficient evidence in the provided documents to answer this question."`
- **Citation Attribution**: Every factual claim is tagged with:
  `[Source: <filename>, Page: <page>, Score: <similarity>]`.

### Task 3: Multi-Tool Autonomous AI Agent
- **Reasoning Framework**: ReAct (Reasoning + Acting) autonomous cycle (`Thought` -> `Action` -> `Action Input` -> `Observation` -> `Final Answer`).
- **Tool Governance**:
  - `SafeMathCalculator`: Strictly AST-based recursive evaluation. Blocks `eval()`, `exec()`, dunder methods (`__`), imports, and arbitrary system calls.
  - `SafeFileReader`: Strictly jailed inside `safe_workspace/`. Blocks path traversal (`../`), cross-drive escapes, symlinks, and forbidden file extensions.
  - `WebSearchTool`: Sanitized DuckDuckGo query engine with input truncation and control character stripping.
- **Guardrails**: Hard limit of 6 iterations and 30-second timeout to prevent runaway loops. Auditable execution traces recording step index, thought, tool action, input, observation, and duration.

### Task 4: Interactive Full-Stack AI Chatbot with Streamlit
- **UI Framework**: Native Streamlit reactive chat (`st.chat_message`, `st.chat_input`, `st.session_state`).
- **Streaming Engine**: Incremental token streaming generator for responsive user feedback.
- **Persona Architecture**: Configurable system instructions (Staff AI Architect, AppSec Auditor, GenAI Research Tutor).
- **Session State Isolation**: Independent conversational state per browser session with one-click reset and dual-format transcript export (JSON and Markdown).
- **Pipeline Interoperability**: Direct integration adapters connecting to the Task 2 document corpus and Task 3 autonomous tools.
