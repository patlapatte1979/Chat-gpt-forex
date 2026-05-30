"""FastAPI bridge prepared for future MetaTrader 5 demo trading."""
from __future__ import annotations

import os
from typing import Literal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

AUTONOMOUS_ENABLED = os.getenv("AUTONOMOUS_ENABLED", "False").lower() == "true"
KILL_SWITCH_ACTIVE = False

app = FastAPI(title="Chat-gpt-forex MT5 Bridge", version="0.1.0")


class OrderRequest(BaseModel):
    symbol: str = Field(..., examples=["EURUSD"])
    side: Literal["BUY", "SELL"]
    entry: float
    stop_loss: float
    take_profit: float
    lot_size: float = Field(..., gt=0)
    risk_cad: float = Field(..., ge=0)
    mode: Literal["COPILOT", "AUTONOMOUS"] = "COPILOT"
    demo_account: bool = True


@app.get("/health")
def health() -> dict[str, bool | str]:
    return {
        "status": "ok",
        "autonomous_enabled": AUTONOMOUS_ENABLED,
        "kill_switch_active": KILL_SWITCH_ACTIVE,
        "real_orders_enabled": False,
    }


@app.post("/prepare-order")
def prepare_order(order: OrderRequest) -> dict[str, object]:
    """Validate and echo an order plan without sending it to MT5."""
    if KILL_SWITCH_ACTIVE:
        raise HTTPException(status_code=423, detail="Kill switch is active.")
    return {
        "prepared": True,
        "message": "Order prepared for review. No real order was sent.",
        "order": order.model_dump(),
    }


@app.post("/execute-order")
def execute_order(order: OrderRequest) -> dict[str, object]:
    """Blocked by default. Future MetaTrader5 integration belongs here."""
    if KILL_SWITCH_ACTIVE:
        raise HTTPException(status_code=423, detail="Kill switch is active.")
    if not AUTONOMOUS_ENABLED:
        raise HTTPException(status_code=403, detail="Autonomous execution is disabled by default.")
    if order.mode != "AUTONOMOUS" or not order.demo_account:
        raise HTTPException(status_code=403, detail="Execution requires AUTONOMOUS mode on a demo account.")

    # TODO: import MetaTrader5 and send demo orders only after explicit safeguards.
    return {
        "executed": False,
        "message": "Demo execution hook reached, but real MT5 sending is not implemented.",
        "order": order.model_dump(),
    }


@app.post("/emergency-stop")
def emergency_stop() -> dict[str, bool | str]:
    global KILL_SWITCH_ACTIVE
    KILL_SWITCH_ACTIVE = True
    return {"kill_switch_active": True, "message": "Emergency stop activated."}
