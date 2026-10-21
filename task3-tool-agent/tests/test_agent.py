"""
Task 3 Test Suite: Security Sandbox Penetration Testing & Autonomous Agent Loop Verification.
"""

import os
import sys
import pytest

# Add parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tools import SafeMathCalculator, SafeFileReader, WebSearchTool
from agent import AutonomousReActAgent


# ------------------------------------------------------------------------------
# 1. Calculator Security & Pen-Testing
# ------------------------------------------------------------------------------

def test_calculator_valid_math():
    """Verify standard arithmetic and allowed mathematical functions."""
    assert SafeMathCalculator.calculate("2 + 2 * 10") == "22"
    assert SafeMathCalculator.calculate("(100 - 25) / 5") == "15"
    assert SafeMathCalculator.calculate("sqrt(144) + 8") == "20"
    assert SafeMathCalculator.calculate("round(3.14159, 2)") == "3.14"


def test_calculator_rejects_code_injection():
    """Verify security rejection of arbitrary code execution attempts."""
    inj1 = "__import__('os').system('dir')"
    assert "Security Error" in SafeMathCalculator.calculate(inj1)

    inj2 = "eval('10 + 20')"
    assert "Security Error" in SafeMathCalculator.calculate(inj2)

    inj3 = "open('/etc/passwd').read()"
    assert "Security Error" in SafeMathCalculator.calculate(inj3)

    inj4 = "globals()"
    assert "Security Error" in SafeMathCalculator.calculate(inj4)


def test_calculator_division_by_zero():
    """Verify division by zero handles gracefully without crashing."""
    res = SafeMathCalculator.calculate("10 / 0")
    assert "Division by zero" in res


# ------------------------------------------------------------------------------
# 2. File Reader Jail & Path Traversal Pen-Testing
# ------------------------------------------------------------------------------

def test_file_reader_valid_access(tmp_path):
    """Verify reading a legitimate file inside the designated workspace."""
    workspace = tmp_path / "safe"
    workspace.mkdir()
    doc = workspace / "data.txt"
    doc.write_text("Confidential Project Metrics: Q3 Net = 13.5M", encoding="utf-8")

    reader = SafeFileReader(workspace_dir=str(workspace))
    content = reader.read_file("data.txt")
    assert "Confidential Project Metrics" in content


def test_file_reader_blocks_path_traversal(tmp_path):
    """Verify security rejection of directory traversal attempts escaping the jail."""
    workspace = tmp_path / "safe"
    workspace.mkdir()

    reader = SafeFileReader(workspace_dir=str(workspace))

    # Path traversal patterns
    res1 = reader.read_file("../../secret.txt")
    assert "Security Error" in res1
    assert "Path traversal" in res1

    res2 = reader.read_file("..\\..\\windows\\system32\\cmd.exe")
    assert "Security Error" in res2


def test_file_reader_blocks_forbidden_extension(tmp_path):
    """Verify rejection of executable scripts and non-whitelisted extensions."""
    workspace = tmp_path / "safe"
    workspace.mkdir()
    script = workspace / "run.py"
    script.write_text("print('malicious')", encoding="utf-8")

    reader = SafeFileReader(workspace_dir=str(workspace))
    res = reader.read_file("run.py")
    assert "Security Error" in res
    assert "forbidden" in res.lower()


# ------------------------------------------------------------------------------
# 3. Web Search Tool Sanitization
# ------------------------------------------------------------------------------

def test_web_search_sanitization():
    """Verify query sanitization and control character stripping."""
    query = "<script>alert('xss')</script> Python 3.12 release date"
    sanitized = WebSearchTool.sanitize_query(query)
    assert "<script>" not in sanitized
    assert "Python 3.12 release date" in sanitized


# ------------------------------------------------------------------------------
# 4. Agent Autonomous ReAct Loop & Auditable Trace
# ------------------------------------------------------------------------------

def test_agent_compound_hardware_task():
    """Verify agent executes multi-step research and calculation with execution traces."""
    agent = AutonomousReActAgent(provider="mock")
    task = "Inspect server inventory to count GPUs and calculate total memory in Terabytes."
    result = agent.run(task)

    assert result.status == "completed"
    assert result.total_steps >= 2
    assert len(result.steps) >= 2
    assert "512" in result.final_answer or "128" in result.final_answer or "Terabytes" in result.final_answer

    # Verify auditable trace structure
    for step in result.steps:
        assert step.step >= 1
        assert len(step.thought) > 0
        assert step.action in ["calculator", "read_file", "web_search"]
        assert len(step.observation) > 0
        assert step.duration_ms >= 0


def test_agent_compound_financial_task():
    """Verify agent reads local CSV metrics and searches inflation rate."""
    agent = AutonomousReActAgent(provider="mock")
    task = "Read Q3 financial profit, search latest inflation rate, and calculate adjusted profit."
    result = agent.run(task)

    assert result.status == "completed"
    assert result.total_steps >= 2
    assert any(step.action == "read_file" for step in result.steps)
    assert any(step.action == "calculator" for step in result.steps)
    assert "$" in result.final_answer
