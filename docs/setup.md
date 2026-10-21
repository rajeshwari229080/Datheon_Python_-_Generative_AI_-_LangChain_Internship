# Environment Setup & Installation Guide
## ApexAI Engineering Operations Suite

A comprehensive step-by-step setup guide for running and developing the ApexAI Suite across Windows, macOS, and Linux platforms.

---

## 📋 System Prerequisites

- **Python**: Version 3.10, 3.11, or 3.12 (Python 3.12 recommended).
- **Git**: Installed and available in your system path.
- **Operating System**: Windows 10/11, macOS (Apple Silicon or Intel), or Linux (Ubuntu 20.04+).

---

## ⚙️ Installation Steps

### 1. Clone the Repository
```bash
git clone https://github.com/rajeshwari229080/Python-Generative-AI-LangChain-Internship.git
cd Python-Generative-AI-LangChain-Internship
```

### 2. Create and Activate a Virtual Environment

**On Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**On macOS / Linux (Bash/Zsh):**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
Install all required dependencies using the unified requirements file:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 🔑 Environment Configuration

The entire suite includes a **Deterministic Offline Mock Engine** that allows all 4 tasks and test suites to execute immediately with zero external API keys.

To enable live generation using commercial LLMs:
1. Copy the environment template:
   ```bash
   cp .env.example .env
   ```
2. Edit `.env` and provide your API keys:
   ```env
   GEMINI_API_KEY=AIzaSy...
   OPENAI_API_KEY=sk-proj-...
   DEFAULT_LLM_PROVIDER=gemini   # Options: 'gemini' | 'openai' | 'mock'
   ```

---

## 🚀 Running the Applications

### Option A: Using the Master Launcher
```bash
python launcher.py --portal    # Start central SaaS operations portal
python launcher.py --task 1    # Launch Task 1: Structured JSON Extractor
python launcher.py --task 2    # Launch Task 2: Grounded Document RAG
python launcher.py --task 3    # Launch Task 3: Autonomous AI Agent
python launcher.py --task 4    # Launch Task 4: Streamlit Chatbot
python launcher.py --test      # Run all automated pytest suites
```

### Option B: Running Individual Projects Manually
- **Task 1 Web Portal**: `python task1-json-extractor/app.py --serve` (Port 8001)
- **Task 2 Web Portal**: `python task2-document-rag/app.py --serve` (Port 8002)
- **Task 3 Interactive CLI**: `python task3-tool-agent/main.py --interactive`
- **Task 4 Streamlit Chatbot**: `streamlit run task4-streamlit-chatbot/app.py` (Port 8501)
