"""Market realism calibration helpers for demo simulations.

The goal is not to predict the future. The goal is to make synthetic and replay
training less toy-like by measuring realistic movement, volatility, spread,
gaps and session behavior from historical candles.
"""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from math import log, sqrt
from statistics import mean, pstdev

from simulation.no_lookahead_replay import Candle


@dataclass(frozen=True)
class RealismProfile:
    symbol: str
    timeframe: str
    sample_size: int
    avg_abs_return: float
    return_stdev: float
    annualized_volatility: float | None
    avg_true_range: float
    max_gap: float
    avg_spread: float
    session_volatility: dict[str, float] = field(default_factory=dict)


@dataclass(frozen=True)
class StressScenario:
    name: str
    volatility_multiplier: float
    spread_multiplier: float
    gap_multiplier: float
    description: str


STRESS_SCENARIOS: tuple[StressScenario, ...] = (
    StressScenario("normal_market", 1.0, 1.0, 1.0, "Baseline calibrated from recent historical candles."),
    StressScenario("quiet_range", 0.55, 0.9, 0.5, "Slow range market with weak movement and false signals."),
    StressScenario("high_volatility_news", 2.4, 3.0, 3.5, "News-like stress with fast moves and wider spread."),
    StressScenario("trend_day", 1.45, 1.1, 1.2, "Directional session where late entries can suffer."),
    StressScenario("choppy_market", 1.7, 1.6, 2.0, "Noisy market with fast reversals and difficult fills."),
)


def build_realism_profile(candles: list[Candle], periods_per_year: int | None = None) -> RealismProfile:
    """Measure realistic movement statistics from historical candles."""
    if len(candles) < 2:
        raise ValueError("At least two candles are required to build a realism profile.")

    ordered = sorted(candles, key=lambda item: item.time)
    symbol = ordered[-1].symbol
    timeframe = ordered[-1].timeframe
    returns: list[float] = []
    true_ranges: list[float] = []
    gaps: list[float] = []
    spreads: list[float] = []
    returns_by_session: dict[str, list[float]] = defaultdict(list)

    previous_close = ordered[0].close
    for candle in ordered[1:]:
        if previous_close <= 0 or candle.close <= 0:
            value_return = 0.0
        else:
            value_return = log(candle.close / previous_close)
        returns.append(value_return)
        true_ranges.append(max(candle.high - candle.low, abs(candle.high - previous_close), abs(candle.low - previous_close)))
        gaps.append(abs(candle.open - previous_close))
        spreads.append(candle.spread)
        returns_by_session[_session_name(candle)].append(abs(value_return))
        previous_close = candle.close

    stdev = pstdev(returns) if len(returns) > 1 else 0.0
    annualized = stdev * sqrt(periods_per_year) if periods_per_year else None

    return RealismProfile(
        symbol=symbol,
        timeframe=timeframe,
        sample_size=len(ordered),
        avg_abs_return=mean(abs(value) for value in returns),
        return_stdev=stdev,
        annualized_volatility=annualized,
        avg_true_range=mean(true_ranges),
        max_gap=max(gaps) if gaps else 0.0,
        avg_spread=mean(spreads) if spreads else 0.0,
        session_volatility={session: mean(values) for session, values in returns_by_session.items() if values},
    )


def _session_name(candle: Candle) -> str:
    """Approximate market session by UTC hour."""
    hour = candle.time.hour
    if 0 <= hour < 7:
        return "asia"
    if 7 <= hour < 13:
        return "london"
    if 13 <= hour < 21:
        return "new_york"
    return "rollover"


def recommended_periods_per_year(timeframe: str) -> int | None:
    tf = timeframe.upper()
    values = {
        "M1": 252 * 24 * 60,
        "M5": 252 * 24 * 12,
        "M15": 252 * 24 * 4,
        "M30": 252 * 24 * 2,
        "H1": 252 * 24,
        "H4": 252 * 6,
        "D1": 252,
    }
    return values.get(tf)
