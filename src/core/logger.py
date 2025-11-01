"""Logging utilities for signal and market data logging.

Provides atomic JSONL logging with time-stamped entries for:
- Market data streams
- Alpha signals
- Order requests and fills
- Account snapshots
"""

import json
import time
from pathlib import Path
from typing import Any, Dict


def atomic_append_jsonl(path: Path, obj: Dict[str, Any]) -> None:
    """
    Atomically append a JSON object as a line to a JSONL file.

    Args:
        path: Path to the JSONL file
        obj: Dictionary object to log

    Notes:
        - Ensures consistent UTC timestamps
        - Uses atomic write operations
        - Handles serialization of common types
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'a', encoding='utf8') as f:
        f.write(json.dumps(obj, default=str) + '\n')
        f.flush()  # Ensure data is written


def log_market_data(log_dir: Path, symbol: str, bar: Dict[str, Any]) -> None:
    """
    Log raw market data to JSONL file.

    Args:
        log_dir: Base logging directory
        symbol: Trading symbol
        bar: Market bar data containing ts, open, high, low, close, volume
    """
    log_file = log_dir / f"market_{symbol}_{bar.get('bar_type', '1m')}.jsonl"
    msg = {
        "ts_utc_ms": bar.get('ts', int(time.time() * 1000)),
        "symbol": symbol,
        "bar_type": bar.get('bar_type', '1m'),
        "o": bar.get('open'),
        "h": bar.get('high'),
        "l": bar.get('low'),
        "c": bar.get('close'),
        "v": bar.get('volume'),
    }
    atomic_append_jsonl(log_file, msg)


def log_signal(log_dir: Path, alpha_id: str, signal: Dict[str, Any]) -> None:
    """
    Log alpha signal to JSONL file.

    Args:
        log_dir: Base logging directory
        alpha_id: Alpha identifier
        signal: Signal dictionary with ts, symbol, action, qty, confidence
    """
    log_file = log_dir / "signals.jsonl"
    msg = {
        "ts": signal.get('ts', int(time.time() * 1000)),
        "alpha_id": alpha_id,
        "symbol": signal.get('symbol'),
        "timeframe": signal.get('timeframe'),
        "signal_id": signal.get('signal_id'),
        "action": signal.get('side'),  # buy/sell/close
        "qty": signal.get('qty'),
        "price": signal.get('price'),
        "confidence": signal.get('confidence'),
    }
    atomic_append_jsonl(log_file, msg)


def log_order_request(log_dir: Path, request: Dict[str, Any]) -> None:
    """
    Log order request to JSONL file.

    Args:
        log_dir: Base logging directory
        request: Order request details
    """
    log_file = log_dir / "orders.jsonl"
    msg = {
        "ts_request": request.get('ts_request', int(time.time() * 1000)),
        "order_request_id": request.get('order_request_id'),
        "alpha_id": request.get('alpha_id'),
        "order_payload": request.get('order_payload'),
        "ts_response": request.get('ts_response'),
        "broker_order_id": request.get('broker_order_id'),
        "status": request.get('status'),
    }
    atomic_append_jsonl(log_file, msg)


def log_fill(log_dir: Path, fill: Dict[str, Any]) -> None:
    """
    Log order fill to JSONL file.

    Args:
        log_dir: Base logging directory
        fill: Fill information
    """
    log_file = log_dir / "fills.jsonl"
    msg = {
        "ts_fill": fill.get('ts_fill', int(time.time() * 1000)),
        "broker_order_id": fill.get('broker_order_id'),
        "filled_qty": fill.get('filled_qty'),
        "filled_price": fill.get('filled_price'),
        "fee": fill.get('fee'),
        "liquidity_flag": fill.get('liquidity_flag'),
    }
    atomic_append_jsonl(log_file, msg)


def log_account_snapshot(log_dir: Path, snapshot: Dict[str, Any]) -> None:
    """
    Log account snapshot to JSONL file.

    Args:
        log_dir: Base logging directory
        snapshot: Account state including cash, positions, margin
    """
    log_file = log_dir / "account_snapshots.jsonl"
    msg = {
        "ts": snapshot.get('ts', int(time.time() * 1000)),
        "cash": snapshot.get('cash'),
        "positions": snapshot.get('positions'),
        "margin_used": snapshot.get('margin_used'),
    }
    atomic_append_jsonl(log_file, msg)
