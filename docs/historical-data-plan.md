# Historical data plan for realistic demo simulation

Goal: train and test demo agents with market movement that feels close to live conditions, while keeping the no-lookahead rule.

## Core idea

Use two data modes:

1. Historical replay
   - Load 3 to 5 years of real candle data when available.
   - Release candles one by one through `NoLookaheadReplay`.
   - Agents only see past and current candles.
   - Results are calculated after decisions.

2. Calibrated simulation
   - Measure real historical movement statistics.
   - Generate realistic demo scenarios using those measurements.
   - Avoid toy charts that move too smoothly or too perfectly.

## First markets

- EUR/USD
- USD/CAD
- GBP/USD
- XAU/USD
- WTI or Brent, depending on source availability
- NAS100 or SPX500, depending on source availability

## Timeframes

- Scalping: M1, M5
- Day trading: M15, H1
- Swing: H4, D1
- Position: D1, W1

## Local CSV format

Large historical datasets should stay local in `data/historical/`. That folder is ignored by Git.

Minimum CSV columns:

```csv
time,symbol,timeframe,open,high,low,close,volume,bid,ask
2024-01-01T09:30:00+00:00,USDCAD,M1,1.35000,1.35040,1.34980,1.35020,100,1.35015,1.35025
```

## Realism metrics

`simulation/market_realism.py` measures:

- average absolute movement;
- return standard deviation;
- annualized volatility when timeframe is known;
- average true range;
- largest gap;
- average spread;
- approximate session behavior: Asia, London, New York, rollover.

## Scenario families

Agents should be tested against multiple regimes:

- normal market;
- quiet range;
- high-volatility event;
- directional trend day;
- choppy market.

## Honest evaluation

Use walk-forward testing:

```text
Training/calibration period
Validation period
Final untouched test period
```

Do not tune the system on the final test period. The final test is used only to estimate how the system behaves on unseen data.

## Safety rules

- No API keys in GitHub.
- No large/licensed datasets in GitHub.
- Real order execution remains disabled.
- Demo and paper trading first.
- Keep stop loss, take profit, kill switch and risk limits active.
