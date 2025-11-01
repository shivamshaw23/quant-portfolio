#!/usr/bin/env python3
"""Compare sandbox/live results with replay backtest results.

Generates results.json file comparing PnL and trades between
live and replay runs for replication verification.
"""

import json
import argparse
from pathlib import Path
from typing import Dict, Any, List


def load_jsonl(file_path: Path) -> List[Dict[str, Any]]:
    """Load JSONL file and return list of records."""
    if not file_path.exists():
        return []

    records = []
    with open(file_path, 'r') as f:
        for line in f:
            records.append(json.loads(line))
    return records


def calculate_pnl(fills: List[Dict[str, Any]]) -> float:
    """Calculate total PnL from fills."""
    # TODO: Implement proper PnL calculation
    # For now, simple placeholder
    return sum(fill.get('filled_qty', 0) * fill.get('filled_price', 0) for fill in fills)


def compare_fills(live_fills: List[Dict], replay_fills: List[Dict]) -> Dict[str, Any]:
    """Compare fills between live and replay runs."""
    comparison = {
        'live_count': len(live_fills),
        'replay_count': len(replay_fills),
        'count_match': len(live_fills) == len(replay_fills),
        'mismatches': [],
    }

    # Compare individual fills
    for i, (live, replay) in enumerate(zip(live_fills, replay_fills)):
        if abs(live.get('filled_price', 0) - replay.get('filled_price', 0)) > 0.01:
            comparison['mismatches'].append({
                'fill_index': i,
                'live_price': live.get('filled_price'),
                'replay_price': replay.get('filled_price'),
                'diff': abs(live.get('filled_price', 0) - replay.get('filled_price', 0)),
            })

    return comparison


def compare_runs(live_dir: Path, replay_dir: Path) -> Dict[str, Any]:
    """Compare live and replay run results."""
    # Load fills
    live_fills = load_jsonl(live_dir / 'fills.jsonl')
    replay_fills = load_jsonl(replay_dir / 'fills.jsonl')

    # Load signals
    live_signals = load_jsonl(live_dir / 'signals.jsonl')
    replay_signals = load_jsonl(replay_dir / 'signals.jsonl')

    # Calculate PnL
    live_pnl = calculate_pnl(live_fills)
    replay_pnl = calculate_pnl(replay_fills)

    # Group by alpha
    alphas_comparison = {}
    alpha_ids = set([s.get('alpha_id') for s in live_signals if s.get('alpha_id')])

    for alpha_id in alpha_ids:
        alpha_live_fills = [f for f in live_fills if f.get('alpha_id') == alpha_id]
        alpha_replay_fills = [f for f in replay_fills if f.get('alpha_id') == alpha_id]

        alphas_comparison[alpha_id] = {
            'trades': len(alpha_live_fills),
            'pnl': calculate_pnl(alpha_live_fills),
            'match': 'PASS' if len(alpha_live_fills) == len(alpha_replay_fills) else 'FAIL',
            'analysis': ''
        }

    # Overall comparison
    results = {
        'portfolio_pnl': {
            'sandbox_pnl': round(live_pnl, 2),
            'backtest_pnl': round(replay_pnl, 2),
            'pnl_match': 'PASS' if abs(live_pnl - replay_pnl) < 0.01 else 'FAIL'
        },
        'alphas': alphas_comparison,
        'fills_comparison': compare_fills(live_fills, replay_fills),
    }

    return results


def generate_results_json(live_dir: Path, replay_dir: Path, output_path: Path) -> None:
    """Generate results.json comparing live and replay runs."""
    results = compare_runs(live_dir, replay_dir)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"Results saved to: {output_path}")
    print(f"\nPortfolio PnL Match: {results['portfolio_pnl']['pnl_match']}")
    print(f"Sandbox PnL: {results['portfolio_pnl']['sandbox_pnl']}")
    print(f"Backtest PnL: {results['portfolio_pnl']['backtest_pnl']}")
    print(f"\nAlpha Results:")
    for alpha_id, alpha_results in results['alphas'].items():
        print(f"  {alpha_id}: {alpha_results['match']} (Trades: {alpha_results['trades']}, PnL: {alpha_results['pnl']:.2f})")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Compare live and replay backtest results')
    parser.add_argument('--live-dir', type=Path, required=True, help='Directory with live/sandbox logs')
    parser.add_argument('--replay-dir', type=Path, required=True, help='Directory with replay backtest logs')
    parser.add_argument('--output', type=Path, default=Path('results/results.json'), help='Output results.json path')

    args = parser.parse_args()

    generate_results_json(args.live_dir, args.replay_dir, args.output)


if __name__ == '__main__':
    main()
