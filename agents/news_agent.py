"""News filter agent."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class NewsSignal:
    score: int
    block_trade: bool
    details: dict[str, str | bool]


class NewsAgent:
    """Blocks trades near major news once an economic-calendar API is connected."""

    name = "news"

    def analyze(self, symbol: str, major_news_nearby: bool = False) -> NewsSignal:
        return NewsSignal(
            score=-10 if major_news_nearby else 0,
            block_trade=major_news_nearby,
            details={
                "symbol": symbol,
                "calendar_source": "placeholder_forexfactory_tradingeconomics",
                "major_news_nearby": major_news_nearby,
            },
        )
