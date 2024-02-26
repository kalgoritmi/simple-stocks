"""
Tests targeting Stock model
"""

import unittest

from pydantic import ValidationError

from src.models.stock import Stock
from src.models.stock_type import StockType


class TetsStockModelFixed(unittest.TestCase):
    """
    Fixed stock model test cases
    """

    def test_stock_symbol_exceptions(self):
        """
        Tests exceptions on invalid instantiations involving symbol field
        """
        with self.assertRaises(ValidationError):
            Stock(
                symbol='tea',
                type=StockType.COMMON,
                last_dividend=10.,
                fixed_dividend=None,
                par_value=100,
            )

        with self.assertRaises(ValidationError):
            Stock(
                symbol='Tea',
                type=StockType.COMMON,
                last_dividend=10.,
                fixed_dividend=None,
                par_value=100,
            )

        with self.assertRaises(ValidationError):
            Stock(
                symbol='Teau',
                type=StockType.COMMON,
                last_dividend=10.,
                fixed_dividend=None,
                par_value=100,
            )

        with self.assertRaises(ValidationError):
            Stock(
                symbol='TEAU',
                type=StockType.COMMON,
                last_dividend=10.,
                fixed_dividend=None,
                par_value=100,
            )

        try:
            # upper case three letter matching pattern '^[A-Z]{3}$'
            Stock(
                symbol='TEA',
                type=StockType.COMMON,
                last_dividend=10.,
                fixed_dividend=None,
                par_value=100,
            )
        except ValidationError:
            self.fail("Unexpected failure on valid usage")


    def test_stock_type_exceptions(self):
        """
        Tests exceptions on invalid instantiations involving type field
        """
        with self.assertRaises(ValidationError):
            Stock(
                symbol='TEA',
                type='PRE',
                last_dividend=10.,
                fixed_dividend=None,
                par_value=100,
            )

        with self.assertRaises(ValidationError):
            Stock(
                symbol='TEA',
                type='Pre',
                last_dividend=10.,
                fixed_dividend=None,
                par_value=100,
            )

        try:
            Stock(
                symbol='TEA',
                type=StockType.PREFERRED,
                last_dividend=10.,
                fixed_dividend=None,
                par_value=100,
            )

            Stock(
                symbol='TEA',
                type=StockType.COMMON,
                last_dividend=10.,
                fixed_dividend=None,
                par_value=100,
            )
        except ValidationError:
            self.fail("Unexpected failure on valid usage")

    def test_stock_last_dividend_exceptions(self):
        """
        Tests exceptions on invalid instantiations involving last_dividend field
        """

        # raises exception on non positive floats
        with self.assertRaises(ValidationError):
            Stock(
                symbol='TEA',
                type=StockType.COMMON,
                last_dividend=-5.,
                fixed_dividend=None,
                par_value=100,
            )

        try:
            # must not raise on zero value
            Stock(
                symbol='TEA',
                type=StockType.COMMON,
                last_dividend=0.,
                fixed_dividend=None,
                par_value=100,
            )

            # must not raise on positive float
            Stock(
                symbol='TEA',
                type=StockType.COMMON,
                last_dividend=10.,
                fixed_dividend=None,
                par_value=100,
            )
        except ValidationError:
            self.fail("Unexpected failure on valid usage")

    def test_stock_fixed_dividend_exceptions(self):
        """
        Tests exceptions on invalid instantiations involving fixed_dividend field
        (a percentage value)
        """

        # raises on values less than lower bound 0.
        with self.assertRaises(ValidationError):
            Stock(
                symbol='TEA',
                type=StockType.COMMON,
                last_dividend=10.,
                fixed_dividend=-5.,
                par_value=100,
            )

        # raises on value exeeding upper bound 100.
        with self.assertRaises(ValidationError):
            Stock(
                symbol='TEA',
                type=StockType.COMMON,
                last_dividend=10.,
                fixed_dividend=105.,
                par_value=100,
            )

        try:
            # must not raise on lower bound value
            Stock(
                symbol='TEA',
                type=StockType.COMMON,
                last_dividend=10.,
                fixed_dividend=0.,
                par_value=100,
            )

            # must not raise on upper bound
            Stock(
                symbol='TEA',
                type=StockType.COMMON,
                last_dividend=10.,
                fixed_dividend=100.,
                par_value=100,
            )

            # must not raise on non provided value
            Stock(
                symbol='TEA',
                type=StockType.COMMON,
                last_dividend=10.,
                fixed_dividend=None,
                par_value=100,
            )

        except ValidationError:
            self.fail("Unexpected failure on valid usage")


    def test_stock_par_value_exceptions(self):
        """
        Tests exceptions on invalid instantiations involving par_value field
        """

        # raises exception on non positive floats
        with self.assertRaises(ValidationError):
            Stock(
                symbol='TEA',
                type=StockType.COMMON,
                last_dividend=10.,
                fixed_dividend=None,
                par_value=-100.,
            )

        try:
            # must not raise on zero value
            Stock(
                symbol='TEA',
                type=StockType.COMMON,
                last_dividend=10.,
                fixed_dividend=None,
                par_value=0.,
            )

            # must not raise on positive float
            Stock(
                symbol='TEA',
                type=StockType.COMMON,
                last_dividend=10.,
                fixed_dividend=None,
                par_value=100.,
            )
        except ValidationError:
            self.fail("Unexpected failure on valid usage")

    def test_from_fields_factory(self):
        """
        Tests if stock instantiation from factory from_fields equals the direct instantiation
        """
        self.assertEqual(
            Stock.from_fields('TEA', StockType.COMMON, 10., None, 100.),
            Stock(
                symbol='TEA',
                type=StockType.COMMON,
                last_dividend=10.,
                fixed_dividend=None,
                par_value=100.,
            )
        )
