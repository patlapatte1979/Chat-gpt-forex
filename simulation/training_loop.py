"""Demo training loop connecting replay, MasterAgent and PaperBroker.

This is intentionally conservative: it is for simulation only and never sends
orders to a live broker.
"""
from __future__ import annotations

from collections.abc import Iterable
from dataclasses import asdict
from datetime import datetime, timedelta

from agents.master_agent import MasterAgent
from agents.risk_manager import AccountState
from simulation.market_universe import TradingStyle, get_style_profile
from simulation.no_lookahead_replay import Candle, NoLookaheadReplay
from simulation.paper_broker import DemoOrder, PaperBroker, Side
from simulation.time_acceleration import ReplayClock, ReplaySpeedConfig, build_batch_speed


def run_replay_training(
    candles: Iterable[Candle],
    symbol: str,
    style: TradingStyle = TradingStyle.DAY_TRADING,
    speed_config: ReplaySpeedConfig | None = None,
) -> dict[str, object]:
    """Run a no-lookahead paper-trading replay for one symbol.

    Use VISUAL x1..x100 for dashboard animation. Use BATCH for fastest training.
    Speed controls only affect waiting time; they never change data order and
    never expose future candles to agents.
    """
    profile = get_style_profile(style)
    replay = NoLookaheadReplay(candles, window_size=max(profile.min_history_bars, 250))
    clock = ReplayClock(speed_config or build_batch_speed())
    agent = MasterAgent()
    broker = PaperBroker()
    decisions: list[dict[str, object]] = []

    for step in replay.warmup_steps(profile.min_history_bars):
        broker.on_candle(step.current)

        account_state = AccountState(
            open_positions=len(broker.account.open_positions),
            is_demo_account=True,
            autonomous_enabled=False,
            kill_switch=False,
        )
        decision = agent.decide(
            symbol=symbol,
            closes=list(step.closes),
            account=account_state,
            major_news_nearby=False,
        )
        decision["time"] = step.current.time.isoformat()
        decision["trading_style"] = style.value
        decision["replay_speed"] = clock.config.label
        decisions.append(decision)

        if decision.get("approved") and decision.get("decision") in {"BUY", "SELL"}:
            broker.place_order(
                DemoOrder(
                    symbol=symbol,
                    side=Side(str(decision["decision"])),
                    lot_size=float(decision["lot_size"]),
                    stop_loss=float(decision["stop_loss"]),
                    take_profit=float(decision["take_profit"]),
                    risk_cad=float(decision["risk_cad"]),
                    strategy=style.value,
                ),
                step.current,
            )

        clock.wait_after_step()

    return {
        "mode": "PAPER_DEMO_REPLAY_NO_LOOKAHEAD",
        "replay_speed": clock.config.label,
        "symbol": symbol,
        "style": style.value,
        "starting_balance": broker.account.starting_balance,
        "ending_balance": broker.account.balance,
        "realized_pnl": broker.account.realized_pnl,
        "open_positions": len(broker.account.open_positions),
        "closed_positions": len(broker.account.closed_positions),
        "decisions": decisions,
        "closed_trades": [asdict(position) for position in broker.account.closed_positions],
    }


def build_synthetic_demo_candles(symbol: str = "USDCAD", count: int = 300) -> list[Candle]:
    """Create deterministic fake candles for smoke tests only.

    Replace this with MT5 demo/practice data or broker practice data before
    trusting any metric.
    """
    start = datetime(2024, 1, 1, 9, 30)
    price = 1.35
    candles: list[Candle] = []
    for index in range(count):
        drift = 0.00008 if index % 40 < 25 else -0.00012
        open_price = price
        close_price = price + drift
        high = max(open_price, close_price) + 0.00025
        low = min(open_price, close_price) - 0.00025
        candles.append(
            Candle(
                time=start + timedelta(minutes=index),
                symbol=symbol,
                timeframe="M1",
                open=round(open_price, 5),
                high=round(high, 5),
                low=round(low, 5),
                close=round(close_price, 5),
                volume=100 + index,
                bid=round(close_price - 0.00005, 5),
                ask=round(close_price + 0.00005, 5),
            )
        )
        price = close_price
    return candles


if __name__ == "__main__":
    sample = build_synthetic_demo_candles()
    result = run_replay_training(sample, symbol="USDCAD", style=TradingStyle.SCALPING)
    print({key: value for key, value in result.items() if key not in {"decisions", "closed_trades"}})
