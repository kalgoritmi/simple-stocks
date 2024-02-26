"""
Formulas
"""

from datetime import datetime
from itertools import tee
from typing import Optional

from pydantic import PositiveFloat, PositiveInt

from src.models.stock_type import StockType
from src.date_utilities import timestamp_n_minutes_ago


class StockScalarFormulasMixin:
    """
    Mixin class providing implementations of scalar formulas for a stock
    """

    def dividend_yield(self, price: PositiveFloat) -> PositiveFloat:
        """
        Calculates dividend yield of stock for a given price
        """
        print(self.type)
        match self.type:
            case StockType.COMMON:
                return self.last_dividend / price
            case StockType.PREFERRED:
                print('hye')
                return (self.par_value * self.fixed_dividend) / price

    def pe_ratio(self, price: PositiveFloat) -> Optional[PositiveFloat]:
        """
        Calculates P/E ratio for a given price
        """
        return price / self.last_dividend if self.last_dividend > 0 else None


class TradeDBVectorFormulasMixin:
    """
    Mixin class providing implementations of vector formulas for trade db
    """

    def gbce_all_share_index(self) -> PositiveFloat:
        """
        Calculates geometric mean of recorded trade prices for all stocks
        """
        product: PositiveFloat = 1.0
        for trade in self:
            product *= trade.price
        return product ** (1 / len(self))

    def volume_weighted_stock_price(
        self,
        symbol: str,
        mock_ts: datetime | None = None
    ) -> PositiveFloat | None:
        """
        Calculates volume weighted stock price formula for all
        recorded trades of a given stock
        """
        n_minutes: PositiveInt = 15
        ts_min_ago = timestamp_n_minutes_ago(n_minutes, mock_ts)
        stock_trades_it = tee(
            filter(
                lambda trade: trade.symbol == symbol \
                    and trade.timestamp >= ts_min_ago,
                self
            ),
            3
        )
        total_quantity = sum(trade.quantity for trade in stock_trades_it[0])

        try:
            next(stock_trades_it[1])  # raises StopIteration if no value yielded
            # do price * frequency to avoid quickly overflowing
            return sum(
                (trade.quantity / total_quantity) * trade.price
                for trade in stock_trades_it[2]
            )
        except StopIteration as exc:
            raise ValueError(
                f'Stock symbol {symbol} has no associated trade in'
                f' last {n_minutes} minutes'
            ) from exc
        except ZeroDivisionError as exc:
            raise ValueError('Total quantity of shares for stock is zero') from  exc