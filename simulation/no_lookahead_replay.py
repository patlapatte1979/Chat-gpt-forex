"""No-lookahead market replay engine for demo agent training.

The replay engine releases candles one at a time. Agents only receive the visible
history available at that moment. Future candles stay hidden until the clock
advances.
"""
from __future__ import annotations

from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Candle:
    time: datetime
    symbol: str
    timeframe: str
    open: float
    high: float
    low: float
    close: float
    volume: float = 0.0
    bid: float | None = None
    ask: float | None = None

    @property
    def spread(self) -> float:
        if self.bid is None or self.ask is None:
            return 0.0
        return max(0.0, self.ask - self.bid)


@dataclass(frozen=True)
class ReplayStep:
    index: int
    current: Candle
    visible_history: tuple[Candle, ...]
    closes: tuple[float, ...]


class NoLookaheadReplay:
    """Iterates through candles without exposing future data."""

    def __init__(self, candles: Iterable[Candle], window_size: int = 250) -> None:
        if window_size < 2:
            raise ValueError("window_size must be at least 2 candles.")
        self.window_size = window_size
        self._candles = tuple(sorted(candles, key=lambda item: item.time))
        self._validate_order()

    def _validate_order(self) -> None:
        for previous, current in zip(self._candles, self._candles[1:]):
            if previous.time > current.time:
                raise ValueError("Candles must be sorted by ascending time.")

    def __iter__(self) -> Iterator[ReplayStep]:
        for index, current in enumerate(self._candles):
            start = max(0, index + 1 - self.window_size)
            visible = self._candles[start : index + 1]
            yield ReplayStep(
                index=index,
                current=current,
                visible_history=visible,
                closes=tuple(candle.close for candle in visible),
            )

    def warmup_steps(self, min_history_bars: int) -> Iterator[ReplayStep]:
        """Yield only steps that have enough visible history for indicators."""
        for step in self:
            if len(step.visible_history) >= min_history_bars:
                yield step

    def __len__(self) -> int:
        return len(self._candles)


def assert_no_future_visible(step: ReplayStep, all_candles: tuple[Candle, ...]) -> None:
    """Safety assertion useful in tests and future training loops."""
    future_times = {candle.time for candle in all_candles[step.index + 1 :]}
    visible_times = {candle.time for candle in step.visible_history}
    leaked = visible_times.intersection(future_times)
    if leaked:
        raise AssertionError(f"Future candles leaked into visible history: {leaked}")
