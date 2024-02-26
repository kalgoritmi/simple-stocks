"""
Implements an in-memory singleton Trade DB
"""

import gc
from pathlib import Path
from typing import Iterable, Iterator, List, Sequence, Union

from src.models.trade import Trade, TradeWithTimestamp
from src.formulas.formulas import TradeDBVectorFormulasMixin

class _TradeDB(Sequence, TradeDBVectorFormulasMixin):
    """
    Sequence of stock trades
    """
    __trades: List[TradeWithTimestamp] = []

    def __init__(self, trades: Iterable[Trade] | None = None):
        if trades is not None:
            self.__trades = trades

    def __contains__(self, value: str) -> bool:
        return any(filter(lambda trade: trade.symbol == value, self.__trades))

    def __getitem__(self, idx: int) -> Trade:
        return self.__trades[idx]

    def add(self, trade: Trade | TradeWithTimestamp):
        "Add trade to db"
        # pylint: disable=C0123
        if type(trade) == Trade:
            self.__trades.append(TradeWithTimestamp.from_trade(trade))
        else:
            self.__trades.append(trade)

    def clear(self):
        self.__trades.clear()

    def __iadd__(self, trade: Trade) -> "_TradeDB":
        self.add(trade)
        return self

    def __iter__(self) -> Iterator:
        return iter(self.__trades)

    def __len__(self) -> int:
        return len(self.__trades)

    def __repr__(self):
        return f"TradeDB(\n\t{'\n\t'.join(repr(trade) for trade in self.__trades)}\n)"

    @classmethod
    def create(cls, path: Union[Path, str] | None) -> "_TradeDB":
        """
        Create an empty StockDB or create and populate from file
        """
        return cls(Trade.from_csv(path)) if path is not None else cls()

class TradeDB:
    """
    Singleton wrapper
    """
    __instance: _TradeDB | None = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = _TradeDB()
        return cls.__instance

    @classmethod
    def reset(cls):
        """
        Clear and reset DB
        """
        cls.__instance.clear()
        gc.collect()
        cls.__instance = None
        print(cls.__instance)

    @classmethod
    def create(cls, path: Union[Path, str] | None) -> "TradeDB":
        """
        Overrides create with singleton specific logic
        """
        if cls.__instance is not None:
            raise AssertionError(
                f"Class {cls.__name__} must only have 1 instance"
            )
        cls.__instance = _TradeDB.create(path)
        return cls.__instance
