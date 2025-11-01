"""Mean reversion alpha based on instrument pair z-score.

This alpha implements a pairs trading strategy using statistical arbitrage
principles. It monitors the z-score of the spread between two correlated
instruments and generates signals when the spread deviates significantly.
"""

from .alpha_base import AlphaBase


class AlphaPairs(AlphaBase):
    """Mean reversion strategy on instrument pair z-score."""

    def __init__(self, alpha_id: str, symbol: str, timeframe: str, params: dict):
        """
        Initialize pairs trading alpha.

        Args:
            alpha_id: Unique identifier for this alpha instance
            symbol: Primary trading symbol (e.g., 'BTCUSDT')
            timeframe: Timeframe for the strategy (e.g., '1m', '5m')
            params: Strategy parameters including:
                - pair_symbol: Secondary symbol for the pair
                - z_lookback: Lookback period for z-score calculation
                - entry_threshold: Z-score threshold for entry (e.g., 2.0)
                - exit_threshold: Z-score threshold for exit (e.g., 0.5)
        """
        super().__init__(alpha_id, symbol, timeframe, params)
        self.state = {
            'position': 0,
            'pair_prices': [],
            'primary_prices': [],
        }

    def on_bar(self, bar: dict) -> dict | None:
        """
        Process market bar and generate pairs trading signals.

        Args:
            bar: Market bar data containing ts, open, high, low, close, volume

        Returns:
            Signal dictionary or None
        """
        # TODO: Implement z-score calculation
        # TODO: Implement entry/exit logic based on z-score thresholds
        # TODO: Track position state
        return None

    def on_fill(self, fill: dict) -> None:
        """
        Handle order fill and update position state.

        Args:
            fill: Fill information including filled_qty, filled_price, etc.
        """
        # TODO: Update position tracking
        # TODO: Log fill for analysis
        pass
