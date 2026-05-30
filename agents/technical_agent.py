"""Technical analysis agent for demo Forex decisions."""
from __future__ import annotations

from dataclasses import dataclass

from strategies.bollinger import score_bollinger_placeholder
from strategies.fibonacci import score_fibonacci_placeholder
from strategies.macd import calculate_macd, score_macd
from strategies.moving_averages import score_ma_cross
from strategies.rsi import calculate_rsi, score_rsi


@dataclass(frozen=True)
class TechnicalSignal:
    score: int
    details: dict[str, float | int | None | str]


class TechnicalAgent:
    """Scores RSI, MACD, MA50/MA200 and safe placeholders from -10 to +10."""

    name = "technical"

    def analyze(self, symbol: str, closes: list[float] | None = None) -> TechnicalSignal:
        closes = closes or []
        rsi_value = calculate_rsi(closes)
        macd_value = calculate_macd(closes)

        raw_score = (
            score_rsi(rsi_value)
            + score_macd(macd_value)
            + score_ma_cross(closes)
            + score_bollinger_placeholder()
            + score_fibonacci_placeholder()
        )
        score = max(-10, min(10, raw_score))
        return TechnicalSignal(
            score=score,
            details={
                "symbol": symbol,
                "rsi": rsi_value,
                "macd_histogram": macd_value["histogram"] if macd_value else None,
                "ma50_ma200": "placeholder_neutral" if len(closes) < 200 else score_ma_cross(closes),
                "adx": "placeholder_neutral",
                "bollinger": "placeholder_neutral",
                "fibonacci": "placeholder_neutral",
            },
        )
