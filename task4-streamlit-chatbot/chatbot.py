"""
Task 4: Interactive Full-Stack AI Chatbot with Streamlit
Core Chatbot Engine managing conversation state, persona prompts, token streaming,
session isolation, and export formatting.
"""

from __future__ import annotations
import os
import json
import time
from typing import List, Dict, Any, Generator, Optional
from datetime import datetime, timezone
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()


class ChatMessage(BaseModel):
    """Represents an atomic message in the conversation history."""
    role: str # "user" | "assistant" | "system"
    content: str
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).strftime("%H:%M:%S"))
    model_used: Optional[str] = None
    trace_info: Optional[List[Dict[str, Any]]] = None


class ChatbotEngine:
    """Manages chat session lifecycle, persona system instructions, and response generation."""

    PERSONAS: Dict[str, str] = {
        "Staff AI Architect": (
            "You are a Staff AI Architect and Senior Systems Engineer. "
            "You provide rigorous, battle-tested software design guidance, architectural diagrams, "
            "and deep evaluations of concurrency, scalability, and distributed systems."
        ),
        "AppSec & Code Auditor": (
            "You are a Principal Application Security Engineer and Senior Code Auditor. "
            "You analyze code for vulnerabilities (OWASP Top 10, injection, deserialization), "
            "recommend defensive patterns, and enforce strict least-privilege standards."
        ),
        "GenAI Research Tutor": (
            "You are a friendly, deeply knowledgeable AI Research Tutor. "
            "You explain complex concepts in Generative AI, RAG, vector embeddings, and agentic loops "
            "with intuitive analogies, clean code examples, and mathematical precision."
        ),
    }

    def __init__(self, provider: Optional[str] = None, persona: str = "Staff AI Architect"):
        self.provider = (provider or os.getenv("DEFAULT_LLM_PROVIDER", "mock")).lower()
        self.active_persona = persona
        self.system_prompt = self.PERSONAS.get(persona, self.PERSONAS["Staff AI Architect"])
        self.history: List[ChatMessage] = []

        self.gemini_key = os.getenv("GEMINI_API_KEY", "")
        self.openai_key = os.getenv("OPENAI_API_KEY", "")

    def set_persona(self, persona_name: str) -> None:
        """Updates active system prompt persona."""
        if persona_name in self.PERSONAS:
            self.active_persona = persona_name
            self.system_prompt = self.PERSONAS[persona_name]

    def add_user_message(self, content: str) -> ChatMessage:
        msg = ChatMessage(role="user", content=content)
        self.history.append(msg)
        return msg

    def clear_history(self) -> None:
        """Resets the conversational session state."""
        self.history.clear()

    def stream_response(self, user_prompt: str) -> Generator[str, None, str]:
        """
        Yields tokens incrementally to provide real-time streaming in Streamlit.
        Returns the complete final accumulated message.
        """
        full_text = ""

        # Live Gemini Streaming
        if self.provider == "gemini" and self.gemini_key and not self.gemini_key.startswith("your_"):
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.gemini_key)
                model = genai.GenerativeModel(
                    "gemini-1.5-flash",
                    system_instruction=self.system_prompt
                )
                response = model.generate_content(user_prompt, stream=True)
                for chunk in response:
                    token = chunk.text or ""
                    full_text += token
                    yield token
                self.history.append(ChatMessage(role="assistant", content=full_text, model_used="google-gemini-1.5"))
                return full_text
            except Exception:
                pass

        # Live OpenAI Streaming
        if self.provider == "openai" and self.openai_key and not self.openai_key.startswith("your_"):
            try:
                from openai import OpenAI
                client = OpenAI(api_key=self.openai_key)
                stream = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": self.system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    stream=True,
                )
                for chunk in stream:
                    delta = chunk.choices[0].delta.content or ""
                    full_text += delta
                    yield delta
                self.history.append(ChatMessage(role="assistant", content=full_text, model_used="openai-gpt-4o-mini"))
                return full_text
            except Exception:
                pass

        # Deterministic Offline Streaming Simulation
        simulated_response = self._synthesize_mock_response(user_prompt)
        words = simulated_response.split(" ")
        for idx, word in enumerate(words):
            token = word + (" " if idx < len(words) - 1 else "")
            full_text += token
            time.sleep(0.02) # Realistic streaming pacing
            yield token

        self.history.append(ChatMessage(role="assistant", content=full_text, model_used="offline-mock-streamer"))
        return full_text

    def _synthesize_mock_response(self, prompt: str) -> str:
        """Synthesizes high-quality, persona-aligned responses deterministically."""
        p_lower = prompt.lower()

        if self.active_persona == "Staff AI Architect":
            if "rag" in p_lower or "retriev" in p_lower:
                return (
                    "When architecting production RAG pipelines, consider separating dense bi-encoders (e.g., ColBERT or BGE) "
                    "from sparse lexical indexes (BM25). Combining both through reciprocal rank fusion (RRF) with cross-encoder "
                    "reranking typically improves NDCG@10 by 24-30% while reducing hallucination risk."
                )
            elif "agent" in p_lower:
                return (
                    "For autonomous agentic orchestration, avoid unrestricted multi-step recursion. Instead, implement a LangGraph "
                    "state machine with hard checkpointing, maximum iteration limits (e.g., 6 steps), and strictly typed Pydantic tools. "
                    "Always enforce safe sandboxes for filesystem and mathematical evaluation."
                )
            else:
                return (
                    f"As a Staff Architect, my recommendation for '{prompt}' is to emphasize modular separation of concerns. "
                    "Decouple state management from provider inference, enforce strict schema contracts using Pydantic v2, "
                    "and implement comprehensive telemetry with OpenTelemetry or Prometheus SLIs."
                )

        elif self.active_persona == "AppSec & Code Auditor":
            return (
                f"Security Audit Analysis for '{prompt}':\n"
                "1. Input Sanitization: Ensure all inbound user telemetry and tool inputs are sanitized against control characters and command injection.\n"
                "2. Sandbox Isolation: Never execute unrestricted eval() or raw shell processes. Confine file readers to canonical jailed directories.\n"
                "3. Principle of Least Privilege: Rotate API keys regularly and store credentials strictly in environment variables, never committed to VCS."
            )

        else: # Research Tutor
            return (
                f"Let's break down '{prompt}' into its core principles!\n"
                "Think of modern LLMs as probabilistic token prediction engines. When we introduce tools or vector search, "
                "we provide factual grounding in the prompt context window, allowing the model to reason over external knowledge "
                "without fine-tuning its weights."
            )

    def export_history_json(self) -> str:
        """Serializes current conversation history as formatted JSON."""
        data = {
            "exported_at": datetime.now(timezone.utc).isoformat(),
            "persona": self.active_persona,
            "provider": self.provider,
            "message_count": len(self.history),
            "messages": [m.model_dump() for m in self.history]
        }
        return json.dumps(data, indent=2)

    def export_history_markdown(self) -> str:
        """Serializes current conversation history as readable Markdown."""
        lines = [
            f"# Conversation Transcript — ApexAI Chatbot",
            f"**Persona**: {self.active_persona} | **Date**: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}",
            f"**Total Messages**: {len(self.history)}\n",
            "---",
            ""
        ]
        for m in self.history:
            sender = "👤 **User**" if m.role == "user" else "🤖 **ApexAI Assistant**"
            lines.append(f"{sender} *({m.timestamp})*:")
            lines.append(m.content)
            lines.append("")
        return "\n".join(lines)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="ApexAI Task 4 Chatbot CLI Runner")
    parser.add_argument("--prompt", "-p", type=str, default="How do we scale vector databases for million-token corpora?", help="User prompt")
    parser.add_argument("--persona", type=str, default="Staff AI Architect", help="Persona name")
    parser.add_argument("--provider", type=str, default=None, help="Provider (gemini, openai, mock)")
    args = parser.parse_args()

    engine = ChatbotEngine(provider=args.provider, persona=args.persona)
    print("=" * 70)
    print(f"  APEX-AI TASK 4 CHATBOT: {args.persona.upper()}")
    print("=" * 70)
    print(f"\nUser: {args.prompt}\n")
    print("Assistant: ", end="", flush=True)
    for token in engine.stream_response(args.prompt):
        print(token, end="", flush=True)
    print("\n\n" + "=" * 70)
    print(f"Status: OK | Persona: {engine.active_persona} | Messages: {len(engine.history)}")
    print("=" * 70)

