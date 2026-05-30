"""Risk manager enforcing demo-first Forex guardrails."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

Decision = Literal["BUY", "SELL", "WAIT"]
Status = Literal["APPROVED", "REJECTED", "WAIT"]
Mode = Literal["COPILOT", "AUTONOMOUS"]


@dataclass(frozen=True)
class RiskConfig:
    account_currency: str = "CAD"
    demo_capital: float = 10_000
    mode: Mode = "COPILOT"
    default_risk_percent: float = 0.5
    max_risk_percent: float = 1.0
    max_daily_loss_percent: float = 1.0
    max_weekly_loss_percent: float = 3.0
    max_open_positions: int = 2
    pause_after_consecutive_losses: int = 3
    minimum_risk_reward: float = 2.0
    preferred_symbols: tuple[str, ...] = ("EURUSD", "USDCAD", "GBPUSD")
    secondary_symbols: tuple[str, ...] = ("XAUUSD",)


@dataclass(frozen=True)
class TradePlan:
    symbol: str
    decision: Decision
    entry: float | None
    stop_loss: float | None
    take_profit: float | None
    lot_size: float = 0.0
    risk_cad: float = 50.0
    risk_reward: float = 0.0


@dataclass(frozen=True)
class AccountState:
    open_positions: int = 0
    daily_loss_percent: float = 0.0
    weekly_loss_percent: float = 0.0
    consecutive_losses: int = 0
    is_demo_account: bool = True
    autonomous_enabled: bool = False
    kill_switch: bool = False


@dataclass(frozen=True)
class RiskResult:
    status: Status
    approved: bool
    reasons: list[str] = field(default_factory=list)
    plan: TradePlan | None = None


class RiskManager:
    """Applies hard risk rules before any order reaches MT5."""

    def __init__(self, config: RiskConfig | None = None) -> None:
        self.config = config or RiskConfig()

    def evaluate(
        self,
        plan: TradePlan,
        account: AccountState | None = None,
        major_news_nearby: bool = False,
        mode: Mode | None = None,
    ) -> RiskResult:
        account = account or AccountState()
        mode = mode or self.config.mode
        reasons: list[str] = []

        if plan.decision == "WAIT":
            return RiskResult(status="WAIT", approved=False, reasons=["Decision is WAIT."], plan=plan)
        if account.kill_switch:
            reasons.append("Kill switch is active.")
        if plan.stop_loss is None:
            reasons.append("Stop loss is mandatory.")
        if plan.take_profit is None:
            reasons.append("Take profit is mandatory.")
        if self.config.default_risk_percent > self.config.max_risk_percent:
            reasons.append("Risk per trade exceeds maximum risk.")
        if plan.risk_reward < self.config.minimum_risk_reward:
            reasons.append("Risk/reward is below 2:1 minimum.")
        if account.open_positions >= self.config.max_open_positions:
            reasons.append("Maximum open positions reached.")
        if account.daily_loss_percent >= self.config.max_daily_loss_percent:
            reasons.append("Maximum daily loss reached.")
        if account.weekly_loss_percent >= self.config.max_weekly_loss_percent:
            reasons.append("Maximum weekly loss reached.")
        if account.consecutive_losses >= self.config.pause_after_consecutive_losses:
            reasons.append("Paused after consecutive losses.")
        if major_news_nearby:
            reasons.append("Blocked before major news.")
        if mode == "AUTONOMOUS" and (not account.is_demo_account or not account.autonomous_enabled):
            reasons.append("AUTONOMOUS mode is allowed only on confirmed demo accounts.")

        approved = not reasons
        return RiskResult(status="APPROVED" if approved else "REJECTED", approved=approved, reasons=reasons, plan=plan)

    def calculate_risk_cad(self) -> float:
        return round(self.config.demo_capital * (self.config.default_risk_percent / 100), 2)
