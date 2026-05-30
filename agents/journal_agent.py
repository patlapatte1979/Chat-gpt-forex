"""CSV journal writer for decisions, errors and lessons."""
from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class JournalAgent:
    """Persists every decision and operational note to CSV files."""

    def __init__(self, journal_dir: str | Path = "journal") -> None:
        self.journal_dir = Path(journal_dir)
        self.journal_dir.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _now() -> str:
        return datetime.now(timezone.utc).isoformat()

    def _append(self, filename: str, row: list[Any]) -> None:
        with (self.journal_dir / filename).open("a", newline="", encoding="utf-8") as handle:
            csv.writer(handle).writerow(row)

    def record_trade(self, decision: dict[str, Any]) -> None:
        self._append(
            "trades.csv",
            [
                self._now(),
                decision.get("symbol"),
                decision.get("mode", "COPILOT"),
                decision.get("decision"),
                decision.get("status"),
                decision.get("entry"),
                decision.get("stop_loss"),
                decision.get("take_profit"),
                decision.get("risk_reward"),
                decision.get("lot_size"),
                decision.get("risk_cad"),
                decision.get("notes", ""),
            ],
        )

    def record_error(self, agent: str, error: Exception | str, context: str = "") -> None:
        self._append("errors.csv", [self._now(), agent, str(error), context])

    def record_lesson(self, symbol: str, lesson: str, source: str = "manual") -> None:
        self._append("lessons.csv", [self._now(), symbol, lesson, source])
