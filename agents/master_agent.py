"""Master agent orchestrating the Forex demo decision workflow."""
from __future__ import annotations

from dataclasses import asdict
from typing import Any

from agents.correlation_agent import CorrelationAgent
from agents.fundamental_agent import FundamentalAgent
from agents.journal_agent import JournalAgent
from agents.news_agent import NewsAgent
from agents.risk_manager import AccountState, RiskManager, TradePlan
from agents.sentiment_agent import SentimentAgent
from agents.technical_agent import TechnicalAgent


class MasterAgent:
    """Calls all agents, aggregates scores and asks RiskManager for approval."""

    def __init__(self) -> None:
        self.technical = TechnicalAgent()
        self.fundamental = FundamentalAgent()
        self.news = NewsAgent()
        self.sentiment = SentimentAgent()
        self.correlation = CorrelationAgent()
        self.risk = RiskManager()
        self.journal = JournalAgent()

    def decide(
        self,
        symbol: str,
        closes: list[float] | None = None,
        account: AccountState | None = None,
        major_news_nearby: bool = False,
    ) -> dict[str, Any]:
        try:
            agent_results = {
                "technical": self.technical.analyze(symbol, closes),
                "fundamental": self.fundamental.analyze(symbol),
                "news": self.news.analyze(symbol, major_news_nearby),
                "sentiment": self.sentiment.analyze(symbol),
                "correlation": self.correlation.analyze(symbol),
            }
            total_score = sum(result.score for result in agent_results.values())
            decision = self._score_to_decision(total_score)
            plan = self._build_demo_plan(symbol, decision)
            risk_result = self.risk.evaluate(
                plan,
                account=account,
                major_news_nearby=agent_results["news"].block_trade,
            )

            payload: dict[str, Any] = {
                "symbol": symbol,
                "mode": self.risk.config.mode,
                "decision": plan.decision,
                "status": risk_result.status,
                "approved": risk_result.approved,
                "total_score": total_score,
                "agent_scores": {name: result.score for name, result in agent_results.items()},
                "risk_reasons": risk_result.reasons,
                "entry": plan.entry,
                "stop_loss": plan.stop_loss,
                "take_profit": plan.take_profit,
                "risk_reward": plan.risk_reward,
                "lot_size": plan.lot_size,
                "risk_cad": plan.risk_cad,
                "notes": "Demo/simulation only. No profit promise.",
            }
            self.journal.record_trade(payload)
            return payload
        except Exception as exc:  # noqa: BLE001 - journal must capture unexpected agent failures.
            self.journal.record_error("master", exc, context=symbol)
            raise

    @staticmethod
    def _score_to_decision(score: int) -> str:
        if score >= 4:
            return "BUY"
        if score <= -4:
            return "SELL"
        return "WAIT"

    def _build_demo_plan(self, symbol: str, decision: str) -> TradePlan:
        demo_prices = {
            "EURUSD": 1.0850,
            "USDCAD": 1.3650,
            "GBPUSD": 1.2750,
            "XAUUSD": 2350.00,
        }
        entry = demo_prices.get(symbol, 1.0)
        if decision == "WAIT":
            return TradePlan(symbol=symbol, decision="WAIT", entry=entry, stop_loss=None, take_profit=None)

        distance = 0.0050 if symbol != "XAUUSD" else 15.0
        stop_loss = entry - distance if decision == "BUY" else entry + distance
        take_profit = entry + (distance * 2) if decision == "BUY" else entry - (distance * 2)
        return TradePlan(
            symbol=symbol,
            decision=decision,  # type: ignore[arg-type]
            entry=round(entry, 5),
            stop_loss=round(stop_loss, 5),
            take_profit=round(take_profit, 5),
            lot_size=0.01,
            risk_cad=self.risk.calculate_risk_cad(),
            risk_reward=2.0,
        )


if __name__ == "__main__":
    sample_closes = [1.07 + (index * 0.0001) for index in range(220)]
    print(asdict(MasterAgent().technical.analyze("EURUSD", sample_closes)))
    print(MasterAgent().decide("EURUSD", sample_closes))
