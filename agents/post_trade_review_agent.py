"""Post-simulation review agent that stores lessons in memory."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from agents.llm_client import OpenAILLMClient, is_llm_available
from agents.memory_store import AgentMemoryStore, Lesson


@dataclass(frozen=True)
class PostTradeReview:
    stored: bool
    lesson: Lesson | None
    details: dict[str, Any]


class PostTradeReviewAgent:
    name = "post_trade_review"

    SYSTEM_PROMPT = """
You review a completed paper/demo trade. Return JSON only with keys:
category, mistake, correction, new_rule, severity. If the trade was acceptable,
use category='none' and severity=0. Do not provide financial advice.
""".strip()

    def __init__(self, memory: AgentMemoryStore | None = None, llm: OpenAILLMClient | None = None) -> None:
        self.memory = memory or AgentMemoryStore()
        self.llm = llm

    def review(self, trade_result: dict[str, Any]) -> PostTradeReview:
        symbol = str(trade_result.get("symbol", "ALL"))
        pnl = float(trade_result.get("pnl_cad", 0.0) or 0.0)

        if not is_llm_available() and self.llm is None:
            if pnl >= 0:
                return PostTradeReview(False, None, {"reason": "No loss and LLM unavailable."})
            lesson = self.memory.add_lesson(
                category="risk_review",
                symbol=symbol,
                mistake="Negative paper result detected without detailed model review.",
                correction="Review entry conditions, stop distance, spread and news filters before next simulation.",
                new_rule="After a negative result, require stronger confirmation and check spread/news filters before the next similar setup.",
                severity=2,
            )
            return PostTradeReview(True, lesson, {"reason": "Fallback lesson stored."})

        client = self.llm or OpenAILLMClient()
        result = client.complete_json(self.SYSTEM_PROMPT, trade_result)
        if int(result.get("severity", 0) or 0) <= 0 or result.get("category") == "none":
            return PostTradeReview(False, None, result)

        lesson = self.memory.add_lesson(
            category=str(result.get("category", "review")),
            symbol=symbol,
            mistake=str(result.get("mistake", "Unspecified issue.")),
            correction=str(result.get("correction", "Review the setup.")),
            new_rule=str(result.get("new_rule", "Require stronger confirmation before repeating this setup.")),
            severity=int(result.get("severity", 1)),
        )
        return PostTradeReview(True, lesson, result)
