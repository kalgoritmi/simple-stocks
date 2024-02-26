"""
Formula tests
"""

import unittest
from datetime import datetime

from pydantic import PositiveFloat

from src.db.trade_db import TradeDB
from src.models.trade import TradeWithTimestamp, TransactionIndicator
from src.date_utilities import timestamp_n_minutes_ago
# initialize, load and import StockDB singleton
# this provides a way to check valid sotcks indexed in GBCE stock exchange
from src.utilities import STOCKS  # pylint: disable=W0611


class TestSingleStockFormulas(unittest.TestCase):
    """
    Test single stock formula mix-ins, these  functions require a price and a stock
    """

    def test_stock_dividend_yield(self):
        """
        Test dividend yield formula
        """

        price: PositiveFloat = 10.

        tea_stock = STOCKS['TEA']  # pylint: disable=E1136
        ale_stock = STOCKS['POP']  # pylint: disable=E1136
        gin_stock = STOCKS['GIN']  # pylint: disable=E1136


        # common types
        self.assertEqual(tea_stock.dividend_yield(price), .0)
        self.assertEqual(ale_stock.dividend_yield(price), .8)

        # preferred type
        self.assertEqual(gin_stock.dividend_yield(price), .2)

    def test_stock_pe_ratio(self):
        """
        Test P/E ratio formula
        """

        price: PositiveFloat = 10.

        tea_stock = STOCKS['TEA']  # pylint: disable=E1136
        ale_stock = STOCKS['POP']  # pylint: disable=E1136
        joe_stock = STOCKS['JOE']  # pylint: disable=E1136

        # common types
        self.assertIsNone(tea_stock.pe_ratio(price))
        self.assertEqual(ale_stock.pe_ratio(price), 1.25)

        # preferred type
        self.assertAlmostEqual(joe_stock.pe_ratio(price), .7692, delta=1e-4)


class TestTradeFormulas(unittest.TestCase):
    """
    Test formula mix-ins
    """

    @classmethod
    def setUpClass(cls) -> None:
        TradeDB()

        cls.ts = datetime.now()  # mock test time

        cls.timestamps = (
            timestamp_n_minutes_ago(12, mock_ts=cls.ts),
            timestamp_n_minutes_ago(30, mock_ts=cls.ts),
            timestamp_n_minutes_ago(15, mock_ts=cls.ts),  # test boundary 15min.
            timestamp_n_minutes_ago(10, mock_ts=cls.ts),
        )
        cls.prices = (10., 34., 62., 70.)
        cls.symbols = ('TEA', 'POP', 'TEA', 'JOE')
        cls.quantities = (50, 10, 32, 1)
        cls.indicators = (
            TransactionIndicator.BUY,
            TransactionIndicator.BUY,
            TransactionIndicator.BUY,
            TransactionIndicator.BUY,
        )

        for args in zip(
            cls.timestamps,
            cls.symbols,
            cls.prices,
            cls.quantities,
            cls.indicators
        ):
            # pylint: disable=E1101
            TradeDB().add(
                TradeWithTimestamp(
                    timestamp=args[0],
                    symbol=args[1],
                    price=args[2],
                    quantity=args[3],
                    indicator=args[4]
                )
            )

    @classmethod
    def tearDownClass(cls):
        TradeDB.reset()

    def test_gbce_index(self):
        """
        Test gbce index on all traded shares based on the geometric mean formula
        """

        print(TradeDB())

        self.assertAlmostEqual(
            TradeDB().gbce_all_share_index(),  # pylint: disable=E1101
            34.8532,
            delta=1e-4
        )

    def test_volume_weighted_stock_price(self):
        """
        Test volume weighted stock price formula
        """

        print(TradeDB())

        self.assertAlmostEqual(
            TradeDB().volume_weighted_stock_price('TEA', self.ts),  # pylint: disable=E1101
            30.29268293,
            delta=1e-4
        )
