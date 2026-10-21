"""
Task 2: Grounded Document Q&A Assistant (RAG)
Grounded RAG Answering Engine with Source Citations and Strict Hallucination Abstention.
"""

from __future__ import annotations
import os
import re
import time
from typing import List, Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv

from retrieval import ResilientCosineVectorIndex, SearchResult
from ingestion import DocumentIngestionEngine
from chunker import RecursiveCharacterChunker, DocumentChunk

load_dotenv()


class Citation(BaseModel):
    """Source attribution for grounded answers."""
    source_file: str
    page_number: int
    chunk_id: str
    relevance_score: float


class RAGResponse(BaseModel):
    """Encapsulates the complete grounded Q&A response payload."""
    question: str
    answer: str
    is_abstention: bool
    citations: List[Citation] = Field(default_factory=list)
    retrieved_chunks: List[SearchResult] = Field(default_factory=list)
    latency_ms: float
    provider_used: str


class GroundedRAGEngine:
    """Orchestrates document ingestion, vector retrieval, grounded answer synthesis, and abstention."""

    ABSTENTION_MESSAGE = "I cannot find sufficient evidence in the provided documents to answer this question."

    def __init__(
        self,
        provider: Optional[str] = None,
        chunk_size: int = 600,
        chunk_overlap: int = 120,
        similarity_threshold: float = 0.20
    ):
        self.provider = (provider or os.getenv("DEFAULT_LLM_PROVIDER", "mock")).lower()
        self.gemini_key = os.getenv("GEMINI_API_KEY", "")
        self.openai_key = os.getenv("OPENAI_API_KEY", "")
        self.similarity_threshold = float(os.getenv("TASK2_SIMILARITY_THRESHOLD", str(similarity_threshold)))

        self.chunker = RecursiveCharacterChunker(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        self.vector_index = ResilientCosineVectorIndex()
        self.indexed_files: List[str] = []

    def ingest_document(self, filepath: str) -> int:
        """Ingests a document file, chunks it, and indexes it into the vector store."""
        pages = DocumentIngestionEngine.load_file(filepath)
        chunks = self.chunker.chunk_document_pages(pages)
        self.vector_index.index_chunks(chunks)
        filename = os.path.basename(filepath)
        if filename not in self.indexed_files:
            self.indexed_files.append(filename)
        return len(chunks)

    def answer_question(self, question: str, top_k: int = 4) -> RAGResponse:
        """Retrieves relevant chunks and generates a grounded response or abstention."""
        start_time = time.perf_counter()

        # Step 1: Vector similarity retrieval
        results = self.vector_index.similarity_search(
            query=question,
            top_k=top_k,
            threshold=self.similarity_threshold
        )

        # Step 2: Check for automatic abstention if no chunks meet threshold
        if not results:
            latency = round((time.perf_counter() - start_time) * 1000, 2)
            return RAGResponse(
                question=question,
                answer=self.ABSTENTION_MESSAGE,
                is_abstention=True,
                citations=[],
                retrieved_chunks=[],
                latency_ms=latency,
                provider_used="rule-based-abstention"
            )

        # Step 3: Format Context and Prompt
        context_blocks = []
        citations: List[Citation] = []
        for r in results:
            chunk = r.chunk
            context_blocks.append(
                f"[Source: {chunk.source_file}, Page: {chunk.page_number}, ChunkID: {chunk.chunk_id}]\n{chunk.text}"
            )
            citations.append(Citation(
                source_file=chunk.source_file,
                page_number=chunk.page_number,
                chunk_id=chunk.chunk_id,
                relevance_score=r.similarity_score
            ))

        formatted_context = "\n\n---\n\n".join(context_blocks)
        prompt = self._build_prompt(question, formatted_context)

        # Step 4: Generate Answer with Live Model or Deterministic Mock
        raw_answer, provider_name = self._synthesize(prompt, question, results)
        latency = round((time.perf_counter() - start_time) * 1000, 2)

        is_abstention = (self.ABSTENTION_MESSAGE.lower() in raw_answer.lower())
        final_citations = [] if is_abstention else citations

        return RAGResponse(
            question=question,
            answer=raw_answer,
            is_abstention=is_abstention,
            citations=final_citations,
            retrieved_chunks=results,
            latency_ms=latency,
            provider_used=provider_name
        )

    def _build_prompt(self, question: str, context: str) -> str:
        return f"""You are a grounded document Q&A assistant.
Your instructions are strict:
1. Answer the question using ONLY facts stated in the Excerpts below.
2. If the excerpts do not contain enough information to answer definitively, you MUST output:
   "{self.ABSTENTION_MESSAGE}"
3. Do not invent, speculate, or extrapolate beyond the provided text.
4. Cite your facts by referencing the source filename and page number.

### Excerpts:
{context}

### Question:
{question}

Answer:"""

    def _synthesize(self, prompt: str, question: str, results: List[SearchResult]) -> tuple[str, str]:
        """Calls configured provider or uses deterministic grounding simulation."""
        # Live Gemini
        if self.provider == "gemini" and self.gemini_key and not self.gemini_key.startswith("your_"):
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.gemini_key)
                model = genai.GenerativeModel("gemini-1.5-flash")
                resp = model.generate_content(prompt)
                return resp.text.strip(), "google-gemini-1.5-flash"
            except Exception:
                pass

        # Live OpenAI
        if self.provider == "openai" and self.openai_key and not self.openai_key.startswith("your_"):
            try:
                from openai import OpenAI
                client = OpenAI(api_key=self.openai_key)
                resp = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.0
                )
                return (resp.choices[0].message.content or "").strip(), "openai-gpt-4o-mini"
            except Exception:
                pass

        # Deterministic Grounding Simulation (Zero API key requirement)
        top_chunk = results[0].chunk
        query_words = set(re.findall(r"\w+", question.lower()))
        chunk_words = set(re.findall(r"\w+", top_chunk.text.lower()))
        common = query_words.intersection(chunk_words)

        # If overlap is too weak, abstain
        if len(common) < 2 and results[0].similarity_score < 0.25:
            return self.ABSTENTION_MESSAGE, "deterministic-offline-mock"

        # Ground answer with citation tag
        first_sentence = top_chunk.text.split(". ")[0] + "."
        answer = (
            f"Based on {top_chunk.source_file} (Page {top_chunk.page_number}): "
            f"{first_sentence} "
            f"[Source: {top_chunk.source_file}, Page {top_chunk.page_number}]"
        )
        return answer, "deterministic-offline-mock"
