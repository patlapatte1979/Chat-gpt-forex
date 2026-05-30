"""Market selector agent for demo simulations."""
from __future__ import annotations

from dataclasses import dataclass

from simulation.market_universe import DEFAULT_MARKETS, AssetClass, MarketInstrument


@dataclass(frozen=True)
class MarketSelectionSignal:
    score: int
    details: dict[str, object]


class MarketSelectorAgent:
    """Chooses which market deserves attention in paper/demo mode."""

    name = "market_selector"

    def analyze(self, symbol: str, preferred_asset_class: AssetClass | None = None) -> MarketSelectionSignal:
        market = self._find_market(symbol)
        if market is None:
            return MarketSelectionSignal(
                score=-2,
                details={"symbol": symbol, "known_market": False, "reason": "symbol_not_in_demo_universe"},
            )

        score = 1
        if preferred_asset_class and market.asset_class == preferred_asset_class:
            score += 1

        return MarketSelectionSignal(
            score=score,
            details={
                "symbol": symbol,
                "known_market": True,
                "asset_class": market.asset_class.value,
                "display_name": market.display_name,
                "preferred_timeframes": market.preferred_timeframes,
                "max_default_spread_points": market.max_default_spread_points,
                "notes": market.notes,
            },
        )

    @staticmethod
    def _find_market(symbol: str) -> MarketInstrument | None:
        normalized = symbol.upper().replace("/", "")
        for market in DEFAULT_MARKETS:
            if market.symbol.upper() == normalized:
                return market
        return None
