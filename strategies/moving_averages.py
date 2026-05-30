"""Moving-average strategy helpers."""
from __future__ import annotations


def simple_moving_average(values: list[float], period: int) -> float | None:
    if len(values) < period:
        return None
    return sum(values[-period:]) / period


def score_ma_cross(closes: list[float], fast: int = 50, slow: int = 200) -> int:
    fast_ma = simple_moving_average(closes, fast)
    slow_ma = simple_moving_average(closes, slow)
    if fast_ma is None or slow_ma is None:
        return 0
    if fast_ma > slow_ma:
        return 3
    if fast_ma < slow_ma:
        return -3
    return 0
