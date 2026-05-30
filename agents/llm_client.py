"""OpenAI client wrapper for real model-backed demo agents.

Keep OPENAI_API_KEY only in environment variables. Never commit secrets.
"""
from __future__ import annotations

import json
import os
from typing import Any

try:
    from openai import OpenAI
except ImportError:  # pragma: no cover - handled at runtime with clear error.
    OpenAI = None  # type: ignore[assignment]


class LLMUnavailableError(RuntimeError):
    """Raised when the OpenAI SDK or API key is unavailable."""


def is_llm_available() -> bool:
    return bool(os.getenv("OPENAI_API_KEY")) and OpenAI is not None


class OpenAILLMClient:
    """Small wrapper around OpenAI for server-side agent reasoning."""

    def __init__(self, model: str | None = None) -> None:
        if OpenAI is None:
            raise LLMUnavailableError("Install dependencies with: pip install -r requirements.txt")
        if not os.getenv("OPENAI_API_KEY"):
            raise LLMUnavailableError("OPENAI_API_KEY is missing from environment variables.")
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
        self.client = OpenAI()

    def complete_json(self, system_prompt: str, user_payload: dict[str, Any]) -> dict[str, Any]:
        """Ask the model for a strict JSON object.

        This is used only for simulation analysis. It must not bypass RiskManager.
        """
        response = self.client.chat.completions.create(
            model=self.model,
            temperature=0.2,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": json.dumps(user_payload, ensure_ascii=False)},
            ],
            response_format={"type": "json_object"},
        )
        content = response.choices[0].message.content or "{}"
        return json.loads(content)
