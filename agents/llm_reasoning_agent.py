"""Model-backed reasoning agent for demo analysis.

The LLM can explain, compare evidence and propose a simulated action. The final
permission still belongs to RiskManager and paper/demo execution only.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from agents.llm_client import OpenAILLMClient, is_llm_available
from agents.memory_store import AgentMemoryStore


@dataclass(frozen=True)
class LLMReasoningSignal:
    score: int
    details: dict[str, Any]


class LLMReasoningAgent:
    name = "llm_reasoning"

    SYSTEM_PROMPT = """
You are a cautious demo-trading reasoning agent. You do not give financial advice.
You analyze only the provided visible market data and memory rules. You never
claim access to future candles or live sources unless the payload explicitly says
those adapters are connected. Return JSON only with keys: score, action,
confidence, explanation, risks, memory_rules_used.
Scores must be integers from -5 to +5. action must be BUY, SELL, or WAIT.
""".strip()

    def __init__(self, memory: AgentMemoryStore | None = None, llm: OpenAILLMClient | None = None) -> None:
        self.memory = memory or AgentMemoryStore()
        self.llm = llm

    def analyze(self, symbol: str, visible_payload: dict[str, Any]) -> LLMReasoningSignal:
        rules = self.memory.rules_for_prompt(symbol=symbol)
        payload = {
            "symbol": symbol,
            "visible_payload": visible_payload,
            "memory_rules": rules,
            "scope": "paper_demo_simulation_only",
        }

        if not is_llm_available() and self.llm is None:
            return LLMReasoningSignal(
                score=0,
                details={
                    "action": "WAIT",
                    "confidence": 0,
                    "explanation": "LLM unavailable. Add OPENAI_API_KEY on the server to enable model-backed reasoning.",
                    "risks": ["No model reasoning available."],
                    "memory_rules_used": rules,
                },
            )

        client = self.llm or OpenAILLMClient()
        result = client.complete_json(self.SYSTEM_PROMPT, payload)
        score = int(result.get("score", 0))
        score = max(-5, min(5, score))
        return LLMReasoningSignal(score=score, details=result)
