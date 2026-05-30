"""Demo-only paper broker for simulated order execution.

This broker never sends real orders. It models balance, positions, spread,
slippage, stop loss and take profit so agents can train in a realistic sandbox.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from uuid import uuid4

from simulation.no_lookahead_replay import Candle


class Side(str, Enum):
    BUY = "BUY"
    SELL = "SELL"


class PositionStatus(str, Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"


@dataclass(frozen=True)
class DemoOrder:
    symbol: str
    side: Side
    lot_size: float
    stop_loss: float
    take_profit: float
    risk_cad: float
    strategy: str = "unknown"


@dataclass
class DemoPosition:
    id: str
    symbol: str
    side: Side
    lot_size: float
    entry_price: float
    stop_loss: float
    take_profit: float
    risk_cad: float
    opened_at: str
    strategy: str = "unknown"
    status: PositionStatus = PositionStatus.OPEN
    exit_price: float | None = None
    closed_at: str | None = None
    pnl_cad: float = 0.0
    exit_reason: str | None = None


@dataclass
class PaperAccount:
    currency: str = "CAD"
    starting_balance: float = 10_000.0
    balance: float = 10_000.0
    equity: float = 10_000.0
    open_positions: list[DemoPosition] = field(default_factory=list)
    closed_positions: list[DemoPosition] = field(default_factory=list)

    @property
    def realized_pnl(self) -> float:
        return round(self.balance - self.starting_balance, 2)


class PaperBroker:
    """Small deterministic paper broker for training loops."""

    def __init__(self, account: PaperAccount | None = None, slippage_points: float = 0.0) -> None:
        self.account = account or PaperAccount()
        self.slippage_points = max(0.0, slippage_points)

    def place_order(self, order: DemoOrder, candle: Candle) -> DemoPosition:
        if order.lot_size <= 0:
            raise ValueError("lot_size must be greater than zero.")
        if order.risk_cad < 0:
            raise ValueError("risk_cad cannot be negative.")

        entry = self._entry_price(order.side, candle)
        position = DemoPosition(
            id=str(uuid4()),
            symbol=order.symbol,
            side=order.side,
            lot_size=order.lot_size,
            entry_price=entry,
            stop_loss=order.stop_loss,
            take_profit=order.take_profit,
            risk_cad=order.risk_cad,
            opened_at=candle.time.isoformat(),
            strategy=order.strategy,
        )
        self.account.open_positions.append(position)
        return position

    def on_candle(self, candle: Candle) -> list[DemoPosition]:
        """Update open positions using only the current released candle."""
        closed: list[DemoPosition] = []
        still_open: list[DemoPosition] = []

        for position in self.account.open_positions:
            if position.symbol != candle.symbol:
                still_open.append(position)
                continue

            exit_price: float | None = None
            reason: str | None = None

            if position.side == Side.BUY:
                if candle.low <= position.stop_loss:
                    exit_price = position.stop_loss
                    reason = "stop_loss"
                elif candle.high >= position.take_profit:
                    exit_price = position.take_profit
                    reason = "take_profit"
            else:
                if candle.high >= position.stop_loss:
                    exit_price = position.stop_loss
                    reason = "stop_loss"
                elif candle.low <= position.take_profit:
                    exit_price = position.take_profit
                    reason = "take_profit"

            if exit_price is None:
                still_open.append(position)
                continue

            self._close_position(position, exit_price, candle, reason or "unknown")
            closed.append(position)

        self.account.open_positions = still_open
        self.account.closed_positions.extend(closed)
        self.account.equity = self.account.balance
        return closed

    def _entry_price(self, side: Side, candle: Candle) -> float:
        spread = candle.spread
        if side == Side.BUY:
            base = candle.ask if candle.ask is not None else candle.close + spread / 2
            return round(base + self.slippage_points, 5)
        base = candle.bid if candle.bid is not None else candle.close - spread / 2
        return round(base - self.slippage_points, 5)

    def _close_position(self, position: DemoPosition, exit_price: float, candle: Candle, reason: str) -> None:
        position.status = PositionStatus.CLOSED
        position.exit_price = round(exit_price, 5)
        position.closed_at = candle.time.isoformat()
        position.exit_reason = reason

        # Conservative simplified payout: losing stop costs the planned risk;
        # winning take profit pays risk * achieved RR.
        if reason == "stop_loss":
            pnl = -abs(position.risk_cad)
        else:
            distance_to_sl = abs(position.entry_price - position.stop_loss)
            distance_to_tp = abs(position.take_profit - position.entry_price)
            rr = distance_to_tp / distance_to_sl if distance_to_sl else 0.0
            pnl = abs(position.risk_cad) * rr

        position.pnl_cad = round(pnl, 2)
        self.account.balance = round(self.account.balance + position.pnl_cad, 2)
