"""
Various helper functions and db initializations
"""

from datetime import datetime, timedelta
from random import random, randrange
from typing import Generator

from pydantic import PositiveFloat

from src.db.stock_db import StockDB

STOCKS: StockDB = StockDB.create(r'gbce.csv')

from src.models.trade import TradeWithTimestamp, TransactionIndicator  # pylint: disable=C0413

from src.db.trade_db import TradeDB  # pylint: disable=C0413

TRADES: TradeDB = TradeDB()


def parse_price(value: str) -> PositiveFloat:
    """
    Parse price to positive float
    Mainly used in the main price prompt
    """
    try:
        return PositiveFloat(value)
    except ValueError as ex:
        raise ValueError('Price should be a positive float') from ex


def gen_k_random_trades(k: int = 5) -> Generator[TradeWithTimestamp, None, None]:
    "Boilerplate random trades generation"
    def random_timestamp():
        return datetime.now() - timedelta(minutes=randrange(60))

    for ts, stock_symbol, stock_price, quantity, indicator in zip(
        (random_timestamp() for _ in range(k)),
        STOCKS.get_k_random_symbols(k),
        (round(100 * random() + 1e-4, 4) for _ in range(k)),
        (randrange(1, 50) for _ in range(k)),
        TransactionIndicator.get_k_random_indicators(k)
    ):
        yield TradeWithTimestamp(
            timestamp=ts,
            symbol=stock_symbol,
            price=stock_price,
            quantity=quantity,
            indicator=indicator
        )
