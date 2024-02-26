"""
Tests targeting Trade DB
"""

import unittest
from datetime import datetime

from src.db.trade_db import TradeDB
from src.models.trade import TradeWithTimestamp, TransactionIndicator
# initialize, load and import StockDB singleton
# this provides a way to check valid stocks indexed in GBCE stock exchange
from src.utilities import STOCKS, gen_k_random_trades  # pylint: disable=W0611


class TestTradeDB(unittest.TestCase):
    """
    Test various operations involving Trade DB
    """

    def setUp(self) -> None:
        TradeDB()  # init

    def tearDown(self) -> None:
        TradeDB.reset()  # clear

    def test_add_trade(self):
        """
        Add a trade in db
        """

        ts = datetime.now()

        trade = TradeWithTimestamp(
            timestamp=ts,
            symbol='TEA',
            price=10.,
            quantity=10,
            indicator=TransactionIndicator.BUY
        )

        TradeDB().add(trade)  # pylint: disable=E1101

        self.assertIn(trade.symbol, TradeDB())

    def test_len_trade(self):
        """
        Test len of db
        """

        for trade in gen_k_random_trades(10):
            TradeDB().add(trade)  # pylint: disable=E1101

        self.assertEqual(len(TradeDB()), 10)
