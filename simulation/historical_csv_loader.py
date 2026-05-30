"""Load historical candle CSV files into the no-lookahead simulator.

Expected minimum columns:
    time,symbol,timeframe,open,high,low,close

Optional columns:
    volume,bid,ask

Keep large or licensed datasets in data/historical/ locally. They are ignored by
Git so the repo stays clean.
"""
from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path

from simulation.no_lookahead_replay import Candle


REQUIRED_COLUMNS = {"time", "symbol", "timeframe", "open", "high", "low", "close"}


def load_candles_csv(path: str | Path) -> list[Candle]:
    csv_path = Path(path)
    if not csv_path.exists():
        raise FileNotFoundError(f"Historical CSV not found: {csv_path}")

    with csv_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise ValueError("CSV file has no header row.")
        missing = REQUIRED_COLUMNS.difference(reader.fieldnames)
        if missing:
            raise ValueError(f"Missing required columns: {sorted(missing)}")

        candles = [_row_to_candle(row) for row in reader]

    return sorted(candles, key=lambda item: item.time)


def _row_to_candle(row: dict[str, str]) -> Candle:
    return Candle(
        time=_parse_datetime(row["time"]),
        symbol=row["symbol"].strip().upper(),
        timeframe=row["timeframe"].strip().upper(),
        open=float(row["open"]),
        high=float(row["high"]),
        low=float(row["low"]),
        close=float(row["close"]),
        volume=float(row.get("volume") or 0.0),
        bid=_optional_float(row.get("bid")),
        ask=_optional_float(row.get("ask")),
    )


def _parse_datetime(value: str) -> datetime:
    clean = value.strip().replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(clean)
    except ValueError as exc:
        raise ValueError(f"Invalid datetime value: {value}") from exc


def _optional_float(value: str | None) -> float | None:
    if value is None or value.strip() == "":
        return None
    return float(value)
