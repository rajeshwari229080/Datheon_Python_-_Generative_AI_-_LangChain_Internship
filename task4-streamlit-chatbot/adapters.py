"""
Task 4: Interactive Full-Stack AI Chatbot with Streamlit
Pipeline adapters connecting the chatbot to Task 2 (Grounded RAG) and Task 3 (Autonomous Tool Agent).
"""

from __future__ import annotations
import os
import sys
from typing import Dict, Any, Optional

# Add workspace root to sys.path to access task2 and task3 modules
workspace_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if workspace_root not in sys.path:
    sys.path.insert(0, workspace_root)


class RAGPipelineAdapter:
    """Provides conversational access to Task 2 Grounded Document RAG."""

    def __init__(self):
        self._engine = None

    def _get_engine(self):
        if self._engine is None:
            from task2_document_rag.rag_engine import GroundedRAGEngine
            self._engine = GroundedRAGEngine(provider="mock")
            # Auto-ingest sample docs
            sample_dir = os.path.join(workspace_root, "task2-document-rag", "samples")
            if os.path.exists(sample_dir):
                for f in os.listdir(sample_dir):
                    if f.endswith((".txt", ".md", ".pdf")):
                        self._engine.ingest_document(os.path.join(sample_dir, f))
        return self._engine

    def query(self, question: str) -> Dict[str, Any]:
        """Queries the RAG engine and formats answer with citations."""
        try:
            # Dynamically import using direct path if needed
            sys.path.insert(0, os.path.join(workspace_root, "task2-document-rag"))
            from rag_engine import GroundedRAGEngine
            engine = GroundedRAGEngine(provider="mock")
            sample_dir = os.path.join(workspace_root, "task2-document-rag", "samples")
            if os.path.exists(sample_dir):
                for f in os.listdir(sample_dir):
                    if f.endswith((".txt", ".md", ".pdf")):
                        engine.ingest_document(os.path.join(sample_dir, f))

            resp = engine.answer_question(question)
            return {
                "answer": resp.answer,
                "is_abstention": resp.is_abstention,
                "citations": [c.model_dump() for c in resp.citations],
                "retrieved_chunks_count": len(resp.retrieved_chunks)
            }
        except Exception as e:
            return {"answer": f"RAG Query Error: {e}", "is_abstention": True, "citations": []}


class ToolAgentPipelineAdapter:
    """Provides conversational access to Task 3 Autonomous Tool Agent."""

    def __init__(self):
        pass

    def execute(self, task_prompt: str) -> Dict[str, Any]:
        """Runs the ReAct autonomous tool agent and returns the final answer with trace steps."""
        try:
            sys.path.insert(0, os.path.join(workspace_root, "task3-tool-agent"))
            from agent import AutonomousReActAgent
            agent = AutonomousReActAgent(provider="mock")
            result = agent.run(task_prompt)
            return {
                "final_answer": result.final_answer,
                "status": result.status,
                "steps": [s.model_dump() for s in result.steps],
                "total_duration_ms": result.total_duration_ms
            }
        except Exception as e:
            return {"final_answer": f"Agent Execution Error: {e}", "status": "error", "steps": []}
