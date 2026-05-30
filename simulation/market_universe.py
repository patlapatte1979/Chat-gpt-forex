"""Market universe and trading styles for demo-only simulations.

This module does not connect to a broker and does not send orders. It only defines
which markets and styles the agents are allowed to evaluate in a paper-trading
or replay environment.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class AssetClass(str, Enum):
    FOREX = "forex"
    METALS = "metals"
    ENERGY = "energy"
    INDICES = "indices"
    CRYPTO = "crypto"


class TradingStyle(str, Enum):
    SCALPING = "scalping"
    DAY_TRADING = "day_trading"
    SWING = "swing"
    POSITION = "position"


@dataclass(frozen=True)
class MarketInstrument:
    symbol: str
    display_name: str
    asset_class: AssetClass
    quote_currency: str
    preferred_timeframes: tuple[str, ...]
    max_default_spread_points: float
    notes: str = ""


@dataclass(frozen=True)
class StyleProfile:
    style: TradingStyle
    timeframes: tuple[str, ...]
    max_hold_minutes: int | None
    min_history_bars: int
    news_blackout_minutes: int
    default_rr: float
    description: str


DEFAULT_MARKETS: tuple[MarketInstrument, ...] = (
    MarketInstrument(
        symbol="EURUSD",
        display_name="EUR/USD",
        asset_class=AssetClass.FOREX,
        quote_currency="USD",
        preferred_timeframes=("M1", "M5", "M15", "H1", "H4"),
        max_default_spread_points=2.0,
        notes="Major forex pair with high liquidity.",
    ),
    MarketInstrument(
        symbol="USDCAD",
        display_name="USD/CAD",
        asset_class=AssetClass.FOREX,
        quote_currency="CAD",
        preferred_timeframes=("M1", "M5", "M15", "H1", "H4"),
        max_default_spread_points=3.0,
        notes="Important for a CAD account and oil-sensitive Canadian dollar context.",
    ),
    MarketInstrument(
        symbol="GBPUSD",
        display_name="GBP/USD",
        asset_class=AssetClass.FOREX,
        quote_currency="USD",
        preferred_timeframes=("M5", "M15", "H1", "H4"),
        max_default_spread_points=3.0,
        notes="Volatile major pair. Scalping requires strict spread control.",
    ),
    MarketInstrument(
        symbol="XAUUSD",
        display_name="Gold / USD",
        asset_class=AssetClass.METALS,
        quote_currency="USD",
        preferred_timeframes=("M5", "M15", "H1", "H4", "D1"),
        max_default_spread_points=35.0,
        notes="Gold can move sharply around USD, yields and risk events.",
    ),
    MarketInstrument(
        symbol="WTIUSD",
        display_name="WTI Oil / USD",
        asset_class=AssetClass.ENERGY,
        quote_currency="USD",
        preferred_timeframes=("M15", "H1", "H4", "D1"),
        max_default_spread_points=8.0,
        notes="Oil exposure is relevant to CAD context; broker symbol may differ.",
    ),
    MarketInstrument(
        symbol="NAS100",
        display_name="Nasdaq 100 CFD",
        asset_class=AssetClass.INDICES,
        quote_currency="USD",
        preferred_timeframes=("M5", "M15", "H1", "H4"),
        max_default_spread_points=20.0,
        notes="Index CFD symbol and contract rules depend on broker.",
    ),
)


STYLE_PROFILES: dict[TradingStyle, StyleProfile] = {
    TradingStyle.SCALPING: StyleProfile(
        style=TradingStyle.SCALPING,
        timeframes=("M1", "M5"),
        max_hold_minutes=45,
        min_history_bars=250,
        news_blackout_minutes=30,
        default_rr=1.5,
        description="Fast decisions. Spread, slippage and execution quality matter most.",
    ),
    TradingStyle.DAY_TRADING: StyleProfile(
        style=TradingStyle.DAY_TRADING,
        timeframes=("M15", "M30", "H1"),
        max_hold_minutes=24 * 60,
        min_history_bars=220,
        news_blackout_minutes=60,
        default_rr=2.0,
        description="Intraday decisions normally closed before the end of the trading day.",
    ),
    TradingStyle.SWING: StyleProfile(
        style=TradingStyle.SWING,
        timeframes=("H4", "D1"),
        max_hold_minutes=10 * 24 * 60,
        min_history_bars=180,
        news_blackout_minutes=180,
        default_rr=2.0,
        description="Multi-day decisions based on trend, levels and macro context.",
    ),
    TradingStyle.POSITION: StyleProfile(
        style=TradingStyle.POSITION,
        timeframes=("D1", "W1"),
        max_hold_minutes=None,
        min_history_bars=120,
        news_blackout_minutes=240,
        default_rr=2.5,
        description="Longer-term decisions. Uses wider stops and macro confirmation.",
    ),
}


def list_markets(asset_class: AssetClass | None = None) -> tuple[MarketInstrument, ...]:
    """Return allowed demo instruments, optionally filtered by asset class."""
    if asset_class is None:
        return DEFAULT_MARKETS
    return tuple(market for market in DEFAULT_MARKETS if market.asset_class == asset_class)


def get_style_profile(style: TradingStyle | str) -> StyleProfile:
    """Return the profile for a trading style."""
    normalized = TradingStyle(style)
    return STYLE_PROFILES[normalized]
