"""Persistent memory store for simulation agents.

This stores lessons, rule updates and post-trade reviews locally as JSONL.
It is not a guarantee that an LLM will never repeat a mistake; it gives agents
retrievable rules and lessons that can be injected into future prompts.
"""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class Lesson:
    created_at: str
    category: str
    symbol: str
    mistake: str
    correction: str
    new_rule: str
    severity: int = 1


class AgentMemoryStore:
    """Append-only local JSONL memory for demo agents."""

    def __init__(self, path: str | Path = "journal/agent_memory.jsonl") -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def add_lesson(
        self,
        category: str,
        symbol: str,
        mistake: str,
        correction: str,
        new_rule: str,
        severity: int = 1,
    ) -> Lesson:
        lesson = Lesson(
            created_at=datetime.now(timezone.utc).isoformat(),
            category=category,
            symbol=symbol,
            mistake=mistake,
            correction=correction,
            new_rule=new_rule,
            severity=severity,
        )
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(asdict(lesson), ensure_ascii=False) + "\n")
        return lesson

    def recent_lessons(self, symbol: str | None = None, limit: int = 20) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        rows: list[dict[str, Any]] = []
        with self.path.open("r", encoding="utf-8") as handle:
            for line in handle:
                if not line.strip():
                    continue
                item = json.loads(line)
                if symbol and item.get("symbol") not in {symbol, "ALL"}:
                    continue
                rows.append(item)
        return rows[-limit:]

    def rules_for_prompt(self, symbol: str | None = None, limit: int = 12) -> list[str]:
        lessons = self.recent_lessons(symbol=symbol, limit=limit)
        return [str(item.get("new_rule", "")).strip() for item in lessons if item.get("new_rule")]
