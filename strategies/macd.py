"""MACD strategy helpers."""
from __future__ import annotations


def _ema(values: list[float], period: int) -> float | None:
    if len(values) < period:
        return None
    multiplier = 2 / (period + 1)
    ema = sum(values[:period]) / period
    for value in values[period:]:
        ema = (value - ema) * multiplier + ema
    return ema


def calculate_macd(closes: list[float]) -> dict[str, float] | None:
    """Return MACD line and signal approximation."""
    if len(closes) < 35:
        return None
    ema_12 = _ema(closes, 12)
    ema_26 = _ema(closes, 26)
    if ema_12 is None or ema_26 is None:
        return None
    macd_line = ema_12 - ema_26

    # Lightweight signal approximation for demo mode.
    recent_macd_values: list[float] = []
    for index in range(26, len(closes) + 1):
        short = _ema(closes[:index], 12)
        long = _ema(closes[:index], 26)
        if short is not None and long is not None:
            recent_macd_values.append(short - long)
    signal = _ema(recent_macd_values, 9) or macd_line
    return {"macd": macd_line, "signal": signal, "histogram": macd_line - signal}


def score_macd(macd: dict[str, float] | None) -> int:
    if macd is None:
        return 0
    if macd["macd"] > macd["signal"]:
        return 2
    if macd["macd"] < macd["signal"]:
        return -2
    return 0
