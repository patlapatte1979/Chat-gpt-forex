# MT5 Bridge

FastAPI bridge for future MetaTrader 5 demo integration.

## Safety defaults

- `AUTONOMOUS_ENABLED=False` by default.
- `/execute-order` blocks autonomous execution unless demo mode and safeguards are explicitly enabled.
- No real order is sent to MetaTrader 5 in this initial version.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn mt5_bridge.mt5_api:app --reload --port 8000
```

## Future MT5 integration

Add the official `MetaTrader5` Python package only after confirming a demo account, risk limits, broker symbol names, order filling mode, and emergency-stop behavior.
