"""Fundamental macro agent placeholder."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FundamentalSignal:
    score: int
    details: dict[str, str]


class FundamentalAgent:
    """Placeholder for FED, ECB and BOC data. Neutral until APIs are connected."""

    name = "fundamental"

    def analyze(self, symbol: str) -> FundamentalSignal:
        return FundamentalSignal(
            score=0,
            details={
                "symbol": symbol,
                "fed": "not_connected_neutral",
                "ecb": "not_connected_neutral",
                "boc": "not_connected_neutral",
            },
        )
