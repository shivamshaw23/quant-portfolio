"""Unit tests for all alpha strategies.

Starter tests for all alpha modules to ensure basic functionality.
"""

import unittest
import sys
sys.path.append('../src')

from src.alphas.alpha_pairs import AlphaPairs
from src.alphas.alpha_breakout import AlphaBreakout
from src.alphas.alpha_mtf import AlphaMTF
from src.alphas.alpha_multi_asset import AlphaMultiAsset
from src.alphas.alpha_orderbook import AlphaOrderbook


class TestAllAlphas(unittest.TestCase):
    """Basic tests for all alpha strategies."""

    def test_alpha_pairs_initialization(self):
        """Test AlphaPairs initialization."""
        alpha = AlphaPairs('test_pairs', 'BTCUSDT', '5m', {})
        self.assertEqual(alpha.alpha_id, 'test_pairs')
        self.assertIsNotNone(alpha.state)

    def test_alpha_breakout_initialization(self):
        """Test AlphaBreakout initialization."""
        alpha = AlphaBreakout('test_breakout', 'ETHUSDT', '15m', {})
        self.assertEqual(alpha.alpha_id, 'test_breakout')
        self.assertIsNotNone(alpha.state)

    def test_alpha_mtf_initialization(self):
        """Test AlphaMTF initialization."""
        alpha = AlphaMTF('test_mtf', 'BTCUSDT', '1m', {})
        self.assertEqual(alpha.alpha_id, 'test_mtf')
        self.assertIsNotNone(alpha.state)

    def test_alpha_multi_asset_initialization(self):
        """Test AlphaMultiAsset initialization."""
        alpha = AlphaMultiAsset('test_multi', 'EURUSD', '5m', {})
        self.assertEqual(alpha.alpha_id, 'test_multi')
        self.assertIsNotNone(alpha.state)

    def test_alpha_orderbook_initialization(self):
        """Test AlphaOrderbook initialization."""
        alpha = AlphaOrderbook('test_orderbook', 'BTCUSDT', 'tick', {})
        self.assertEqual(alpha.alpha_id, 'test_orderbook')
        self.assertIsNotNone(alpha.state)

    def test_all_alphas_on_bar_interface(self):
        """Test that all alphas implement on_bar interface."""
        alphas = [
            AlphaPairs('test1', 'BTCUSDT', '5m', {}),
            AlphaBreakout('test2', 'ETHUSDT', '15m', {}),
            AlphaMTF('test3', 'BTCUSDT', '1m', {}),
            AlphaMultiAsset('test4', 'EURUSD', '5m', {}),
            AlphaOrderbook('test5', 'BTCUSDT', 'tick', {})
        ]
        bar = {
            'ts': 1609459200000,
            'open': 29000.0,
            'high': 29100.0,
            'low': 28900.0,
            'close': 29050.0,
            'volume': 10.5
        }
        for alpha in alphas:
            # Should return None (or dict) without raising exception
            result = alpha.on_bar(bar)
            self.assertTrue(result is None or isinstance(result, dict))


if __name__ == '__main__':
    unittest.main()
