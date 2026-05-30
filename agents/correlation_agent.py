"""Correlation agent placeholder."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CorrelationSignal:
    score: int
    details: dict[str, str]


class CorrelationAgent:
    """Placeholder for DXY, gold and major USD-pair correlation checks."""

    name = "correlation"

    def analyze(self, symbol: str) -> CorrelationSignal:
        return CorrelationSignal(
            score=0,
            details={
                "symbol": symbol,
                "dxy": "not_connected_neutral",
                "gold": "not_connected_neutral",
                "usdcad": "not_connected_neutral",
                "eurusd": "not_connected_neutral",
            },
        )
