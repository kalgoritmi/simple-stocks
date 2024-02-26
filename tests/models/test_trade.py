"""
Tests targeting Trade and TradeWithStamp models
"""

from datetime import datetime
import unittest

from pydantic import ValidationError

# initialize, load and import StockDB singleton
# this provides a way to check valid sotcks indexed in GBCE stock exchange
from src.utilities import STOCKS  # pylint: disable=W0611

from src.models.trade import Trade, TradeWithTimestamp, TransactionIndicator


class TetsTradeModelFixed(unittest.TestCase):
    """
    Fixed trade model test cases
    """

    def test_trade_symbol_exceptions(self):
        """
        Tests exceptions on invalid instantiations involving symbol field
        """

        # raises if symbol is not in Stock DB
        # DEW is not a registered beverage in GBCE
        with self.assertRaises(ValidationError):
            Trade(
                symbol='DEW',
                price=10.,
                quantity=10,
                indicator=TransactionIndicator.BUY,
            )

        try:
            Trade(
                symbol='TEA',
                price=10.,
                quantity=10,
                indicator=TransactionIndicator.BUY,
            )
        except ValidationError:
            self.fail("Unexpected failure on valid usage")

    def test_trade_price_exceptions(self):
        """
        Tests exceptions on invalid instantiations involving price field
        """

        # raises on price being negative
        with self.assertRaises(ValidationError):
            Trade(
                symbol='TEA',
                price=-10.,
                quantity=10,
                indicator=TransactionIndicator.BUY,
            )

        # raises on price being zero
        with self.assertRaises(ValidationError):
            Trade(
                symbol='TEA',
                price=0.,
                quantity=10,
                indicator=TransactionIndicator.BUY,
            )

        try:
            Trade(
                symbol='TEA',
                price=10.,
                quantity=10,
                indicator=TransactionIndicator.BUY,
            )
        except ValidationError:
            self.fail("Unexpected failure on valid usage")

    def test_trade_quantity_exceptions(self):
        """
        Tests exceptions on invalid instantiations involving quantity field
        """

        # raises on quantity being negative
        with self.assertRaises(ValidationError):
            Trade(
                symbol='TEA',
                price=10.,
                quantity=-10,
                indicator=TransactionIndicator.BUY,
            )

        # raises on quantity being zero
        with self.assertRaises(ValidationError):
            Trade(
                symbol='TEA',
                price=10.,
                quantity=0,
                indicator=TransactionIndicator.BUY,
            )

        try:
            Trade(
                symbol='TEA',
                price=10.,
                quantity=10,
                indicator=TransactionIndicator.BUY,
            )
        except ValidationError:
            self.fail("Unexpected failure on valid usage")

    def test_trade_indicator_exceptions(self):
        """
        Tests exceptions on invalid instantiations involving buy or sell indicator field
        """

        # raises on random value
        with self.assertRaises(ValidationError):
            Trade(
                symbol='TEA',
                price=10.,
                quantity=10,
                indicator='trade',
            )

        try:
            Trade(
                symbol='TEA',
                price=10.,
                quantity=10,
                indicator=TransactionIndicator.BUY,
            )

            Trade(
                symbol='TEA',
                price=10.,
                quantity=10,
                indicator=TransactionIndicator.SELL,
            )

        except ValidationError:
            self.fail("Unexpected failure on valid usage")

    def test_trade_from_fields_exceptions(self):
        """
        Tests from_fields factory method
        """

        self.assertEqual(
            Trade(
                symbol='TEA',
                price=10.,
                quantity=10,
                indicator=TransactionIndicator.BUY,
            ),
            Trade.from_fields('TEA', 10., 10, TransactionIndicator.BUY)
        )


class TetsTradeWithTimestampModelFixed(unittest.TestCase):
    """
    Fixed trade with timestamp model test cases
    """

    def test_trade_with_ts_from_trade_exceptions(self):
        """
        Tests from_trade factory method
        """

        ts = datetime.now()

        # test timestamp mocking
        self.assertEqual(
            TradeWithTimestamp(
                timestamp=ts,
                symbol='TEA',
                price=10.,
                quantity=10,
                indicator=TransactionIndicator.BUY,
            ),
            TradeWithTimestamp.from_trade(
                Trade.from_fields('TEA', 10., 10, TransactionIndicator.BUY),
                mock_timestamp=ts,
            )
        )

