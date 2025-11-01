# Quant Portfolio - Alpha Development & Deployment

## Project Overview

Multi-asset algorithmic trading system with 5 independent alpha strategies, event-driven backtesting, hyperparameter optimization, and deployment with replay verification.

## Branch: alpha-backtest-deploy

This branch implements Phases II-IV:
- **Phase II**: Alpha Development & Portfolio
- **Phase III**: Backtesting, HPT, WFO
- **Phase IV**: Deployment & Replication

---

## Project Structure

```
quant-portfolio/
├── src/
│   ├── alphas/           # Alpha strategies
│   │   ├── alpha_base.py          # Base class interface
│   │   ├── alpha_pairs.py         # Mean reversion pairs
│   │   ├── alpha_breakout.py      # Volatility breakout
│   │   ├── alpha_mtf.py           # Multi-timeframe momentum
│   │   ├── alpha_multi_asset.py   # Cross-asset signals
│   │   └── alpha_orderbook.py     # L2 microstructure
│   ├── core/
│   │   └── logger.py              # JSONL logging utilities
│   ├── backtest/
│   │   └── backtest_engine.py     # Event-driven backtesting
│   ├── hpt/
│   │   └── hpt_optuna.py          # Hyperparameter tuning
│   ├── brokers/
│   └── deploy/
├── tests/
│   ├── test_alpha_pairs.py
│   └── test_all_alphas.py         # Unit tests for all alphas
├── results/
│   ├── tools/
│   │   └── compare_replay.py      # Replay verification script
│   ├── market_data/               # Raw JSONL market data
│   ├── signals.jsonl              # Alpha signal log
│   ├── fills.jsonl                # Execution fills
│   └── results.json               # Final comparison results
├── docs/
│   └── final_report.pdf           # (To be generated)
├── configs/
├── notebooks/
├── docker-compose.yml
├── Dockerfile
└── README.md
```

---

## Phase II: Alpha Development

### Alpha Interface (AlphaBase)

All alpha strategies inherit from `AlphaBase` with standardized interface:

```python
class AlphaBase:
    def __init__(self, alpha_id, symbol, timeframe, params):
        # Initialize with strategy parameters
    
    def on_bar(self, bar: dict) -> dict | None:
        # Process market bar and return signal or None
        # bar = {ts, open, high, low, close, volume}
        # signal = {side:'buy'|'sell', qty, confidence, price}
    
    def on_fill(self, fill: dict) -> None:
        # Handle fill and update internal state
```

### Five Alpha Strategies

1. **alpha_pairs.py**: Mean reversion on instrument pair z-score
2. **alpha_breakout.py**: Volatility breakout strategy
3. **alpha_mtf.py**: Multi-timeframe momentum (1m + 1h)
4. **alpha_multi_asset.py**: Cross-asset correlation (FX vs equity)
5. **alpha_orderbook.py**: L2 order book microstructure

### Logging Format

All logs use timestamped JSONL format:

**Market Data** (`market_{symbol}_{timeframe}.jsonl`):
```json
{"ts_utc_ms": 1609459200000, "symbol": "BTCUSDT", "bar_type": "1m", 
 "o": 29000.0, "h": 29100.0, "l": 28900.0, "c": 29050.0, "v": 12.3}
```

**Signals** (`signals.jsonl`):
```json
{"ts": 1609459200000, "alpha_id": "alpha_pairs", "symbol": "BTCUSDT",
 "signal_id": "sig_001", "action": "buy", "qty": 1.0, "confidence": 0.85}
```

**Fills** (`fills.jsonl`):
```json
{"ts_fill": 1609459200000, "broker_order_id": "order_123", 
 "filled_qty": 1.0, "filled_price": 29050.0, "fee": 0.01, "liquidity_flag": "taker"}
```

---

## Phase III: Backtesting & Optimization

### Backtesting Engine

Event-driven backtesting with replay mode:

```python
from src.backtest.backtest_engine import BacktestEngine, ReplayEngine

config = {
    'start_date': '2024-01-01',
    'end_date': '2024-12-31',
    'initial_capital': 100000,
    'data_path': 'results/market_data'
}
engine = BacktestEngine(config)
results = engine.run_backtest(alphas)
```

### Hyperparameter Tuning (Optuna)

Example for `alpha_pairs`:

```python
from src.hpt.hpt_optuna import AlphaHPT

param_space = {
    'z_lookback': ('int', 10, 200),
    'entry_threshold': ('float', 1.5, 3.0),
    'exit_threshold': ('float', 0.3, 1.0)
}

hpt = AlphaHPT(AlphaPairs, backtest_function, config)
results = hpt.run_optimization(param_space, n_trials=100)
hpt.save_study(Path('results/hpt/alpha_pairs_hpt.json'))
```

### Walk-Forward Optimization

- Rolling windows: 12 months IS / 3 months OOS
- Tune parameters on IS data
- Apply to OOS and record performance
- Generate IS vs OOS equity curves

---

## Phase IV: Deployment & Replication

### Sandbox Run

1. Start Docker deployment:
```bash
docker-compose up -d
```

2. Run live trading (sandbox):
```bash
python src/deploy/run_live.py --config configs/sandbox.yaml --duration 1week
```

3. Logs automatically saved to `results/live/`

### Replay Backtest

Run replay using recorded data:

```python
from src.backtest.backtest_engine import ReplayEngine

config = {
    'data_path': 'results/live/market_data',  # Use recorded data
    'execution_model': {...},  # Same as live
}

replay = ReplayEngine(config)
replay_results = replay.run_backtest(alphas)
```

### Verification

Compare live vs replay:

```bash
python results/tools/compare_replay.py \
    --live-dir results/live \
    --replay-dir results/replay \
    --output results/results.json
```

**results.json Format**:
```json
{
  "portfolio_pnl": {
    "sandbox_pnl": 572.30,
    "backtest_pnl": 572.30,
    "pnl_match": "PASS"
  },
  "alphas": {
    "alpha_pairs": {"trades": 15, "pnl": 102.50, "match": "PASS"},
    "alpha_breakout": {"trades": 8, "pnl": -30.10, "match": "PASS"},
    "alpha_mtf": {"trades": 12, "pnl": 210.40, "match": "PASS"},
    "alpha_multi_asset": {"trades": 3, "pnl": 301.00, "match": "PASS"},
    "alpha_orderbook": {"trades": 55, "pnl": -11.50, "match": "FAIL", 
                        "analysis": "L2 book update latency mismatch"}
  }
}
```

---

## Testing

Run all tests:
```bash
pytest tests/
python -m unittest tests.test_all_alphas
```

---

## CI/CD

GitHub Actions workflow:
- Run unit tests
- Code formatting (black, flake8)
- Build Docker image
- Deploy on merge to main

---

## Quick Start

1. **Clone and setup**:
```bash
git clone https://github.com/shivamshaw23/quant-portfolio.git
cd quant-portfolio
git checkout alpha-backtest-deploy
pip install -r requirements.txt
```

2. **Run tests**:
```bash
pytest tests/
```

3. **Run backtest**:
```bash
python src/backtest/backtest_engine.py --config configs/backtest.yaml
```

4. **Run HPT**:
```bash
python src/hpt/hpt_optuna.py
```

5. **Deploy sandbox**:
```bash
docker-compose up -d
python src/deploy/run_live.py --config configs/sandbox.yaml
```

6. **Verify replay**:
```bash
python results/tools/compare_replay.py --live-dir results/live --replay-dir results/replay
```

---

## Key Features

✅ **5 Independent Alpha Strategies** with standardized interface  
✅ **Event-Driven Backtesting** with exact replay capability  
✅ **Hyperparameter Optimization** using Optuna  
✅ **Walk-Forward Optimization** for robust validation  
✅ **Comprehensive Logging** (JSONL format, atomic writes)  
✅ **Replay Verification** for deployment confidence  
✅ **Docker Deployment** for reproducibility  
✅ **Unit Tests** for all alpha modules  

---

## Documentation

See `docs/final_report.pdf` for:
- Architecture diagrams
- Mathematical alpha definitions
- Backtest & WFO results
- Replication analysis (results.json explanation)

---

## License

MIT License
