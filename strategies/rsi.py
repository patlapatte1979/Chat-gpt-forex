"""RSI strategy helpers."""
from __future__ import annotations


def calculate_rsi(closes: list[float], period: int = 14) -> float | None:
    """Return a simple RSI value, or None when data is insufficient."""
    if len(closes) <= period:
        return None

    gains: list[float] = []
    losses: list[float] = []
    for previous, current in zip(closes[-period - 1 : -1], closes[-period:]):
        change = current - previous
        gains.append(max(change, 0.0))
        losses.append(abs(min(change, 0.0)))

    average_gain = sum(gains) / period
    average_loss = sum(losses) / period
    if average_loss == 0:
        return 100.0

    relative_strength = average_gain / average_loss
    return 100 - (100 / (1 + relative_strength))


def score_rsi(rsi: float | None) -> int:
    """Score RSI from bearish (-) to bullish (+)."""
    if rsi is None:
        return 0
    if rsi < 30:
        return 3
    if rsi > 70:
        return -3
    return 0
