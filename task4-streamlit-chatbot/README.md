# Task 4: Interactive Full-Stack AI Chatbot with Streamlit
## ApexAI Engineering Operations Suite

A reactive conversational interface built with Streamlit featuring real-time token streaming, session state isolation, conversation history persistence, persona switching, and seamless integration with the Task 2 (RAG) and Task 3 (Autonomous Tool Agent) pipelines.

---

## 🚀 Key Features

1. **Streamlit Reactive Conversational UI**:
   - Built natively with `st.chat_message`, `st.chat_input`, and `st.session_state`.
   - Real-time token streaming with visual typing indicators and timing telemetry.
2. **Dynamic Persona Presets**:
   - **Staff AI Architect**: Systems engineering, distributed design patterns, and scalability evaluations.
   - **AppSec & Code Auditor**: OWASP Top 10 analysis, input sanitization, and defensive programming.
   - **GenAI Research Tutor**: Intuitive pedagogical explanations of vector embeddings, RAG, and agentic loops.
3. **Session State Isolation & History Export**:
   - Isolated conversational state per session.
   - One-click session reset (`🗑️ Clear Conversation`).
   - Dual-format transcript export: formatted JSON and human-readable Markdown.
4. **Pipeline Interoperability**:
   - Integrated adapters connecting to Task 2 (Grounded RAG) for document citations.
   - Integrated adapters connecting to Task 3 (Autonomous ReAct Agent) for multi-step tools.
5. **Dual Provider & Deterministic Streaming**:
   - Live streaming via Google Gemini or OpenAI GPT-4o-mini when API keys are configured.
   - Deterministic offline token streamer for instant offline evaluation.

---

## 📁 Directory Structure

```text
task4-streamlit-chatbot/
├── app.py                   # Streamlit reactive web user interface
├── chatbot.py               # ChatbotEngine, session manager, and streaming
├── adapters.py              # RAG and Autonomous Agent pipeline adapters
├── requirements.txt         # Standalone dependencies
├── README.md                # Task 4 documentation
└── tests/                   # Pytest automated test suite
    ├── __init__.py
    └── test_chatbot.py
```

---

## 🛠️ Usage Instructions

### 1. Launching the Chatbot
Start the Streamlit application:
```bash
streamlit run task4-streamlit-chatbot/app.py
```
Open **`http://localhost:8501`** in your browser.

- Select an active persona from the left sidebar.
- Enter questions or discussion topics in the chat input at the bottom.
- Observe real-time streaming token generation.
- Click **Export JSON** or **Export Markdown** to download the conversation transcript.
- Click **Clear Conversation** to reset session state.

---

## 🧪 Running Automated Tests

Run the automated test suite:
```bash
pytest task4-streamlit-chatbot/tests -v
```
Expected output: 7 passing tests validating session state defaults, persona updates, streaming generator output, transcript serialization, and pipeline adapter hooks.
