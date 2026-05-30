"""Trading style selector for demo agents."""
from __future__ import annotations

from dataclasses import dataclass

from simulation.market_universe import TradingStyle, get_style_profile


@dataclass(frozen=True)
class StyleSelectionSignal:
    score: int
    details: dict[str, object]


class StyleSelectorAgent:
    """Selects scalping, day trading, swing or position context."""

    name = "style_selector"

    def analyze(self, requested_style: TradingStyle | str = TradingStyle.DAY_TRADING) -> StyleSelectionSignal:
        profile = get_style_profile(requested_style)
        return StyleSelectionSignal(
            score=1,
            details={
                "style": profile.style.value,
                "timeframes": profile.timeframes,
                "max_hold_minutes": profile.max_hold_minutes,
                "min_history_bars": profile.min_history_bars,
                "news_blackout_minutes": profile.news_blackout_minutes,
                "default_rr": profile.default_rr,
                "description": profile.description,
            },
        )
