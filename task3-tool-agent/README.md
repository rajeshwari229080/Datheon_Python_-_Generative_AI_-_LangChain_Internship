# Task 3: Multi-Tool Autonomous AI Agent
## ApexAI Engineering Operations Suite

An autonomous ReAct (Reasoning + Acting) AI agent capable of decomposing and executing compound research and computational tasks across three strictly governed, sandboxed tools with an auditable step-by-step trace and safety guardrails.

---

## 🚀 Key Features

1. **Autonomous ReAct Reasoning Loop**:
   - Iterative cycle: `Thought` (goal formulation) -> `Action` (tool dispatch) -> `Action Input` (sanitized argument) -> `Observation` (tool output) -> `Final Answer`.
2. **Three Strictly Governed Tools**:
   - **AST-Based Math Calculator**: Evaluates expressions using Python's `ast` module. **Strictly zero `eval()` or `exec()`**. Blocks dunders (`__`), imports, builtins, and system calls.
   - **Jailed Local File Reader**: Confined strictly to `safe_workspace/`. Blocks path traversal (`../`, absolute system paths, symlinks) and non-whitelisted extensions.
   - **Sanitized Web Search**: DuckDuckGo search with query length caps, control character filtering, and network timeout fallbacks.
3. **Enterprise Safety Guardrails**:
   - `max_iterations`: Hard cap (default: 6) preventing runaway recursive loops.
   - `timeout_seconds`: Hard execution timeout (default: 30s).
   - Auditable Execution Trace: Logs step index, thought, tool action, input, observation, and millisecond duration for every tool call. Internal system prompt secrets are never leaked.
4. **Dual Provider & Deterministic Mock Planner**:
   - Executes live model function calling with Gemini or OpenAI.
   - Includes an autonomous deterministic simulation planner for zero-key evaluation.

---

## 📁 Directory Structure

```text
task3-tool-agent/
├── main.py                  # CLI runner and interactive trace dashboard
├── agent.py                 # AutonomousReActAgent engine
├── requirements.txt         # Standalone dependencies
├── README.md                # Task 3 documentation
├── tools/                   # Sandboxed tool implementations
│   ├── __init__.py
│   ├── safe_calculator.py   # AST-based safe math evaluator
│   ├── safe_file_reader.py  # Jailed file reader with traversal blocking
│   └── web_search.py        # Sanitized DuckDuckGo search tool
├── safe_workspace/          # Sandboxed local directory
│   ├── company_handbook.md
│   ├── q3_financial_metrics.csv
│   └── server_inventory.txt
└── tests/                   # Pytest automated test suite
    ├── __init__.py
    └── test_agent.py
```

---

## 🛠️ Usage Instructions

### 1. Interactive CLI Mode
Launch the interactive agent console:
```bash
python task3-tool-agent/main.py --interactive
```

Sample compound tasks to try:
```text
agent-prompt > Read the server inventory file and calculate total memory in Terabytes.
agent-prompt > Read Q3 financial profit, search inflation rate, and calculate adjusted profit.
```

### 2. Single-Task Command Mode
Run a specific prompt directly:
```bash
python task3-tool-agent/main.py --task "Read server_inventory.txt and calculate GPU count"
```

---

## 🛡️ Security Audit Verification

1. **Code Injection Attack**:
   - Passing `__import__('os').system('dir')` or `eval("2+2")` to the calculator immediately yields:
     `Security Error: Forbidden token '__' detected.`
2. **Directory Traversal Attack**:
   - Passing `../../windows/system32` or `/etc/passwd` to the file reader yields:
     `Security Error: Path traversal attack detected!`
3. **Execution Guardrails**:
   - ReAct loops automatically terminate at 6 iterations with full trace logging.

---

## 🧪 Running Automated Tests

Run the security and agent test suite:
```bash
pytest task3-tool-agent/tests -v
```
Expected output: 9 passing tests verifying calculator AST safety, code injection rejections, directory jail traversal blocks, web query sanitization, and multi-step compound task execution traces.
