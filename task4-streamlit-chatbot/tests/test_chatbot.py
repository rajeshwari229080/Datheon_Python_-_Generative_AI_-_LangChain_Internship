"""
Task 4 Test Suite: Chatbot Session Management, Streaming, and History Export.
"""

import os
import sys
import json
import pytest

# Add parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from chatbot import ChatbotEngine, ChatMessage
from adapters import RAGPipelineAdapter, ToolAgentPipelineAdapter


def test_chatbot_session_initialization():
    """Verify session initialization and persona defaults."""
    engine = ChatbotEngine()
    assert engine.active_persona == "Staff AI Architect"
    assert len(engine.history) == 0
    assert "Staff AI Architect" in engine.system_prompt


def test_chatbot_persona_switching():
    """Verify updating persona updates active instructions."""
    engine = ChatbotEngine()
    engine.set_persona("AppSec & Code Auditor")
    assert engine.active_persona == "AppSec & Code Auditor"
    assert "Security Engineer" in engine.system_prompt


def test_chatbot_message_history():
    """Verify adding messages updates history sequentially."""
    engine = ChatbotEngine()
    msg = engine.add_user_message("Hello, architect!")
    assert msg.role == "user"
    assert msg.content == "Hello, architect!"
    assert len(engine.history) == 1

    engine.clear_history()
    assert len(engine.history) == 0


def test_chatbot_streaming_generator():
    """Verify response streaming generator yields tokens and accumulates response."""
    engine = ChatbotEngine(provider="mock")
    tokens = list(engine.stream_response("Explain vector indexing"))

    assert len(tokens) > 1
    full_text = "".join(tokens)
    assert len(full_text) > 20
    assert len(engine.history) == 1
    assert engine.history[0].role == "assistant"
    assert engine.history[0].content == full_text


def test_chatbot_export_formats():
    """Verify JSON and Markdown transcript export serialization."""
    engine = ChatbotEngine(provider="mock")
    engine.add_user_message("What is RAG?")
    list(engine.stream_response("What is RAG?"))

    # Test JSON export
    json_str = engine.export_history_json()
    data = json.loads(json_str)
    assert data["message_count"] == 2
    assert data["persona"] == "Staff AI Architect"
    assert len(data["messages"]) == 2

    # Test Markdown export
    md_str = engine.export_history_markdown()
    assert "# Conversation Transcript" in md_str
    assert "👤 **User**" in md_str
    assert "🤖 **ApexAI Assistant**" in md_str


def test_chatbot_rag_adapter():
    """Verify RAG adapter returns grounded answers from Task 2 corpus."""
    adapter = RAGPipelineAdapter()
    result = adapter.query("What is the meal reimbursement limit?")
    assert "answer" in result
    assert "85" in result["answer"]
    assert not result["is_abstention"]


def test_chatbot_tool_agent_adapter():
    """Verify Tool-Agent adapter executes compound task via Task 3 agent."""
    adapter = ToolAgentPipelineAdapter()
    result = adapter.execute("Read server inventory and calculate GPU count")
    assert result["status"] == "completed"
    assert len(result["steps"]) >= 1
    assert "512" in result["final_answer"] or "GPU" in result["final_answer"]
