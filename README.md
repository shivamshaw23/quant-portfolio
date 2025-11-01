# Quant Portfolio - Phase I: Framework & Broker Connectivity

## Project Structure

```
quant-portfolio/
├─ docs/
├─ configs/
│  ├─ nautilus/
│  └─ local.yaml
├─ src/
│  ├─ core/
│  │  ├─ event_engine.py
│  │  ├─ data_handler.py
│  │  ├─ order_manager.py
│  │  └─ logger.py
│  ├─ brokers/
│  │  ├─ binance_client.py
│  │  ├─ ibkr_client.py
│  │  └─ zerodha_sim.py
│  ├─ alphas/
│  │  ├─ alpha_pairs.py
│  │  ├─ alpha_breakout.py
│  │  └─ ...
│  ├─ backtest/
│  ├─ deploy/
│  └─ utils/
├─ tests/
├─ notebooks/
└─ results/
```

## Quick Setup

Run the setup script to create the project structure:

```bash
python setup_structure.py
```

This will automatically create all necessary directories and starter files.

## Phase I Priorities: Broker Connectivity

### A. Binance Testnet
- Register and generate API keys for Binance Testnet
- Testnet base endpoint: https://testnet.binance.vision/api
- Use Spot Test Network flow
- Implement `binance_client.py` with:
  - REST wrapper for historical bars and order endpoints
  - WebSocket for streaming data
  - UTC epoch ms (or ns) timestamps in logs
- Test placing/canceling orders in testnet
- Example libraries: `python-binance` or `aiohttp` custom wrapper

### B. Interactive Brokers (IBKR) Paper Trading
- Use IB Gateway or TWS in paper mode
- Implement `ibkr_client.py` using:
  - `ibapi` (official IB Python lib) or IB Web API
- Test connecting, requesting market data, and submitting orders to Paper account
- Reference: [IB API Documentation](https://www.interactivebrokers.com/campus/ibkr-api-page/twsapi-doc/)

### C. Zerodha / Kite
- Confirm with instructors about provided sandbox
- If no sandbox available:
  - Create `zerodha_sim.py` with simulated matching engine
  - Replay historical Kite data
  - Accept REST-style order requests
  - Simulate exchange rules
- If sandbox provided, adapt to their endpoints
- Reference: [Kite Connect API](https://zerodha.com/products/api/)

## General Engineering Rules

### Timestamps
- Everything in UTC
- ISO8601 + epoch ms format
- Consistent across all brokers

### Deterministic Seeds
- Seed all RNGs (if using stochastic elements)
- Record seed values

### Idempotency
- Record order request/response pairs
- Use unique IDs for all orders

### Time Synchronization
- Log NTP sync status
- Ensure consistent time across all systems

## Getting Started

1. Set up Python environment (Python 3.8+)
2. Install dependencies: `pip install -r requirements.txt`
3. Run setup script: `python setup_structure.py`
4. Configure broker credentials in `configs/local.yaml`
5. Test broker connectivity with provided test scripts
6. Review engineering guidelines before implementation

## Backtesting Core

**Track B**: This project uses [NautilusTrader](https://github.com/nautechsystems/nautilus_trader) as the backtesting engine.

- NautilusTrader is a high-performance algorithmic trading platform
- Event-driven architecture for realistic backtesting
- Support for multiple asset classes and data feeds
