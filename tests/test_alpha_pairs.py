"""Unit tests for AlphaPairs strategy.

Tests signal generation, position tracking, and z-score calculations
for the pairs trading alpha.
"""

import unittest
from unittest.mock import Mock
import sys
sys.path.append('../src')

from src.alphas.alpha_pairs import AlphaPairs


class TestAlphaPairs(unittest.TestCase):
    """Test cases for AlphaPairs alpha strategy."""

    def setUp(self):
        """Set up test fixtures."""
        self.params = {
            'pair_symbol': 'ETHUSDT',
            'z_lookback': 20,
            'entry_threshold': 2.0,
            'exit_threshold': 0.5,
        }
        self.alpha = AlphaPairs(
            alpha_id='alpha_pairs_test',
            symbol='BTCUSDT',
            timeframe='5m',
            params=self.params
        )

    def test_initialization(self):
        """Test alpha initialization."""
        self.assertEqual(self.alpha.alpha_id, 'alpha_pairs_test')
        self.assertEqual(self.alpha.symbol, 'BTCUSDT')
        self.assertEqual(self.alpha.timeframe, '5m')
        self.assertEqual(self.alpha.state['position'], 0)

    def test_on_bar_returns_none_initially(self):
        """Test that on_bar returns None when insufficient data."""
        bar = {
            'ts': 1609459200000,
            'open': 29000.0,
            'high': 29100.0,
            'low': 28900.0,
            'close': 29050.0,
            'volume': 10.5
        }
        signal = self.alpha.on_bar(bar)
        self.assertIsNone(signal)

    def test_on_fill_updates_state(self):
        """Test that on_fill properly updates internal state."""
        fill = {
            'ts_fill': 1609459200000,
            'broker_order_id': 'order_123',
            'filled_qty': 1.0,
            'filled_price': 29000.0,
            'fee': 0.01,
            'liquidity_flag': 'maker'
        }
        # Should not raise exception
        self.alpha.on_fill(fill)


if __name__ == '__main__':
    unittest.main()
