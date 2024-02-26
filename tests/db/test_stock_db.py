"""
Tests targeting Stock DB
"""

import unittest

from src.models.stock import Stock
from src.models.stock_type import StockType
# initialize, load and import StockDB singleton
# this provides a way to check valid stocks indexed in GBCE stock exchange
from src.utilities import STOCKS  # pylint: disable=W0611


class TestStockDB(unittest.TestCase):
    """
    Test various operations involving Stock DB
    """

    def test_stock_db_symbols(self):
        """
        Test if stock db registered symbols match those of gbce csv
        """

        self.assertEqual(
            STOCKS.symbols(),
            ['TEA', 'POP', 'ALE', 'GIN', 'JOE']
        )

        self.assertNotEqual(
            STOCKS.symbols(),
            ['TEA', 'POP', 'ALE', 'GIN']
        )

    def test_stock_contents(self):
        """
        Asserts listing stock db contents equals fixture
        """
        self.assertListEqual(
            STOCKS.list(),
            [
                Stock.from_fields('TEA', StockType.COMMON, 0., None, 100.),
                Stock.from_fields('POP', StockType.COMMON, 8., None, 100.),
                Stock.from_fields('ALE', StockType.COMMON, 23., None, 60.),
                Stock.from_fields('GIN', StockType.PREFERRED, 8., 2, 100.),
                Stock.from_fields('JOE', StockType.COMMON, 13., None, 250.),
            ]
        )

    def test_add_and_delete_stock(self):
        """
        Test adding and deleting a stock
        """

        stock = Stock.from_fields('FAN', StockType.COMMON, 0., None, 50.)
        STOCKS.add(stock)

        self.assertIn('FAN', STOCKS)
        self.assertEqual(stock, STOCKS['FAN'])  # pylint: disable=E1136

        del STOCKS['FAN']  # pylint: disable=E1136, E1138

        self.assertNotIn('FAN', STOCKS)
