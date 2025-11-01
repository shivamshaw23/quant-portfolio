"""Base class for all alpha strategies.

All alpha modules must inherit from AlphaBase and implement the required interface.
"""


class AlphaBase:
    """Base class for alpha strategies with standardized interface."""

    def __init__(self, alpha_id: str, symbol: str, timeframe: str, params: dict):
        """
        Initialize alpha strategy.

        Args:
            alpha_id: Unique identifier for this alpha instance
            symbol: Trading symbol (e.g., 'BTCUSDT')
            timeframe: Timeframe for the strategy (e.g., '1m', '1h')
            params: Dictionary of strategy-specific parameters
        """
        self.alpha_id = alpha_id
        self.symbol = symbol
        self.timeframe = timeframe
        self.params = params
        self.state = {}

    def on_bar(self, bar: dict) -> dict | None:
        """
        Process market bar and generate trading signals.

        Args:
            bar: Dictionary containing:
                - ts: timestamp (UTC ms)
                - open: open price
                - high: high price
                - low: low price
                - close: close price
                - volume: trading volume

        Returns:
            Signal dictionary or None:
            {
                'side': 'buy' | 'sell' | 'close',
                'qty': float,
                'confidence': float (0.0-1.0),
                'price': float (optional limit price)
            }
        """
        raise NotImplementedError("Subclasses must implement on_bar()")

    def on_fill(self, fill: dict) -> None:
        """
        Handle order fill and update internal state.

        Args:
            fill: Dictionary containing:
                - ts_fill: timestamp of fill (UTC ms)
                - broker_order_id: broker's order ID
                - filled_qty: quantity filled
                - filled_price: execution price
                - fee: transaction fee
                - liquidity_flag: maker/taker flag
        """
        raise NotImplementedError("Subclasses must implement on_fill()")
