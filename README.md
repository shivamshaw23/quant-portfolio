# quant-portfolio

Quantitative trading portfolio for Track B implementation.

## Setup

### Virtual Environment

Create and activate a virtual environment:

```bash
python -m venv .venv && source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Backtesting Core

**Track B**: This project uses [NautilusTrader](https://github.com/nautechsystems/nautilus_trader) as the backtesting engine.

- NautilusTrader is a high-performance algorithmic trading platform
- Event-driven architecture for realistic backtesting
- Support for multiple asset classes and data feeds

### Stack Overview

- **Python**: 3.11+
- **Data Processing**: pandas, numpy
- **Async I/O**: asyncio, aiohttp
- **Database**: sqlalchemy, psycopg2-binary
- **Analytics**: quantstats, pyfolio, matplotlib
- **HPT (Hyperparameter Tuning)**: optuna

## Docker Setup

Services are defined in `docker-compose.yml`:
- PostgreSQL (market data & logs)
- Redis (cache/message bus)
- Kafka (optional, event streaming)
- Worker service

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.
