"""Market sentiment agent placeholder."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SentimentSignal:
    score: int
    details: dict[str, str]


class SentimentAgent:
    """Placeholder for TradingView, X and Reddit sentiment. Neutral by default."""

    name = "sentiment"

    def analyze(self, symbol: str) -> SentimentSignal:
        return SentimentSignal(
            score=0,
            details={
                "symbol": symbol,
                "tradingview": "not_connected_neutral",
                "x": "not_connected_neutral",
                "reddit": "not_connected_neutral",
            },
        )
