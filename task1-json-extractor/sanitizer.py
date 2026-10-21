"""
Task 1: Structured LLM Prompt Pipeline & JSON Extractor
Multi-pass JSON sanitizer and healing pre-parser.
Handles markdown fences, conversational preambles, and trailing commas.
"""

from __future__ import annotations
import re


class JSONSanitizer:
    """Multi-pass healing for noisy LLM outputs."""

    @staticmethod
    def clean(raw_output: str) -> str:
        text = raw_output.strip()

        # Pass 1: Extract content inside markdown fences if present
        fence_match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text, re.IGNORECASE)
        if fence_match:
            text = fence_match.group(1).strip()

        # Pass 2: Extract substring between first '{' and last '}'
        start_idx = text.find("{")
        end_idx = text.rfind("}")
        if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
            text = text[start_idx : end_idx + 1]

        # Pass 3: Clean up common trailing commas before closing braces/brackets
        text = re.sub(r",\s*([\]}])", r"\1", text)
        return text
