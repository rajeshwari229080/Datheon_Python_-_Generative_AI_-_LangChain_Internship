# Python Generative AI & LangChain Internship — Person 1 Suite
## ApexAI Suite: Production-Grade Multi-Task AI Engineering System

[![Python 3.12](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Pydantic v2](https://img.shields.io/badge/Pydantic-v2.10-green.svg)](https://docs.pydantic.dev/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.42-red.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)

An enterprise-ready AI engineering suite built for the **Google Antigravity Python + Generative AI & LangChain Internship**. This repository delivers **Person 1's original, production-grade implementation** across four foundational artificial intelligence competencies, unified by a central SaaS operations portal.

---

## 🏛️ Architecture Overview

The suite is located in [`person1-internship-suite/`](./person1-internship-suite/) and contains four independent, fully tested projects:

```text
person1-internship-suite/
├── index.html                   # Central SaaS Portal & Launcher Dashboard
├── launcher.py                  # CLI Orchestrator & Multi-Project Server
├── requirements.txt             # Unified Suite Dependencies
├── .env.example                 # Configuration & API Key Template
│
├── task1-json-extractor/        # Task 1: Structured LLM Prompt Pipeline & JSON Extractor
│   ├── app.py                   # FastAPI Interactive Web UI & CLI
│   ├── schemas.py               # Pydantic v2 Invoice & Resume Validation Models
│   ├── prompts.py               # Parameterized System Prompts & Few-Shot Exemplars
│   ├── extractor.py             # Multi-pass Sanitizer & LLM Client (Gemini/OpenAI/Mock)
│   ├── samples/                 # Realistic Invoice & Resume Test Documents
│   ├── tests/                   # Automated Pytest Suite
│   └── README.md                # Task 1 Comprehensive Documentation
│
├── task2-document-rag/          # Task 2: Grounded Document Q&A Assistant (RAG)
│   ├── app.py                   # Web UI & Interactive CLI Query Engine
│   ├── ingestion.py             # PDF & Text Document Parsing with Metadata
│   ├── chunker.py               # Recursive Character Semantic Chunker
│   ├── retrieval.py             # Dual Vector Store (ChromaDB / Resilient Vector Index)
│   ├── rag_engine.py            # Grounded Answer Synthesis & Abstention Logic
│   ├── samples/                 # Policies & Technical Whitepapers
│   ├── tests/                   # Pytest Retrieval & Abstention Tests
│   └── README.md                # Task 2 Comprehensive Documentation
│
├── task3-tool-agent/            # Task 3: Multi-Tool Autonomous AI Agent
│   ├── main.py                  # Agent CLI & Interactive Audit Dashboard
│   ├── agent.py                 # ReAct Reasoning Loop with Iteration Guardrails
│   ├── tools/                   # AST Calculator, Jailed File Reader, Web Search
│   ├── safe_workspace/          # Sandboxed Local Filesystem
│   ├── tests/                   # Security Sandbox & Loop Termination Tests
│   └── README.md                # Task 3 Comprehensive Documentation
│
├── task4-streamlit-chatbot/     # Task 4: Interactive Full-Stack AI Chatbot
│   ├── app.py                   # Streamlit Reactive Web UI
│   ├── chatbot.py               # Session State Manager & Streaming Engine
│   ├── adapters.py              # Dynamic RAG and Tool-Calling Integrations
│   ├── tests/                   # Session State & Persona Preset Tests
│   └── README.md                # Task 4 Comprehensive Documentation
│
└── docs/                        # Suite-wide Engineering Specifications
    ├── architecture.md          # End-to-End System Design & Data Flow
    ├── setup.md                 # Cross-Platform Installation & Config Guide
    └── testing.md               # Quality Assurance & Test Verification Report
```

---

## ⚡ Quickstart

### 1. Clone & Set Up Environment
```bash
git clone https://github.com/rajeshwari229080/Python-Generative-AI-LangChain-Internship.git
cd Python-Generative-AI-LangChain-Internship
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r person1-internship-suite/requirements.txt
```

### 2. Configure Environment (Optional for Live Models)
Copy `.env.example` to `.env`. The entire suite functions immediately in **Deterministic Mock Mode** with zero configuration. Add your Gemini or OpenAI API key to enable live generation.
```bash
cp person1-internship-suite/.env.example person1-internship-suite/.env
```

### 3. Launch the Central Operations Portal
Open [`person1-internship-suite/index.html`](./person1-internship-suite/index.html) in any browser or run:
```bash
python person1-internship-suite/launcher.py --portal
```

---

## 🧪 Automated Testing
Run the complete automated test suite across all 4 tasks:
```bash
python -m pytest person1-internship-suite/task1-json-extractor/tests -v
python -m pytest person1-internship-suite/task2-document-rag/tests -v
python -m pytest person1-internship-suite/task3-tool-agent/tests -v
python -m pytest person1-internship-suite/task4-streamlit-chatbot/tests -v
```

---

## 👤 Author & Attribution
- **Internship**: Google Antigravity Python + Generative AI & LangChain Internship
- **Persona**: Person 1 (Independent Implementation & Architecture)
- **Repository**: [rajeshwari229080/Python-Generative-AI-LangChain-Internship](https://github.com/rajeshwari229080/Python-Generative-AI-LangChain-Internship.git)
