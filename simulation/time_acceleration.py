"""Replay time acceleration controls for visual and batch simulations.

Two modes are supported:
- VISUAL: wait between candles so a dashboard can animate the replay at x1..x100.
- BATCH: do not wait; process history as fast as the machine can compute.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from time import sleep


class ReplayRunMode(str, Enum):
    VISUAL = "visual"
    BATCH = "batch"


@dataclass(frozen=True)
class ReplaySpeedConfig:
    speed_multiplier: int = 1
    mode: ReplayRunMode = ReplayRunMode.BATCH
    base_seconds_per_candle: float = 1.0

    def __post_init__(self) -> None:
        if not 1 <= self.speed_multiplier <= 100:
            raise ValueError("speed_multiplier must be between 1 and 100.")
        if self.base_seconds_per_candle <= 0:
            raise ValueError("base_seconds_per_candle must be greater than zero.")

    @property
    def delay_seconds(self) -> float:
        if self.mode == ReplayRunMode.BATCH:
            return 0.0
        return self.base_seconds_per_candle / self.speed_multiplier

    @property
    def label(self) -> str:
        if self.mode == ReplayRunMode.BATCH:
            return "BATCH_FASTEST"
        return f"VISUAL_X{self.speed_multiplier}"


class ReplayClock:
    """Controls replay pacing without changing candle order or exposing future data."""

    def __init__(self, config: ReplaySpeedConfig | None = None) -> None:
        self.config = config or ReplaySpeedConfig()

    def wait_after_step(self) -> None:
        delay = self.config.delay_seconds
        if delay > 0:
            sleep(delay)


def build_visual_speed(speed_multiplier: int, base_seconds_per_candle: float = 1.0) -> ReplaySpeedConfig:
    """Create x1..x100 visual replay speed for UI animation."""
    return ReplaySpeedConfig(
        speed_multiplier=speed_multiplier,
        mode=ReplayRunMode.VISUAL,
        base_seconds_per_candle=base_seconds_per_candle,
    )


def build_batch_speed() -> ReplaySpeedConfig:
    """Create fastest possible training speed with no artificial delay."""
    return ReplaySpeedConfig(speed_multiplier=100, mode=ReplayRunMode.BATCH)
