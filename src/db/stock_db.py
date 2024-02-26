"""
Implements an in-memory singleton Stock DB
"""

import gc
from collections.abc import Mapping
from random import choices

from pathlib import Path
from typing import Dict, Iterable, Iterator, List, Union

from src.models.stock import Stock

class _StockDB(Mapping):
    """
    Map of Stock collections
    """
    __data: Dict[str, Stock] = {}

    def __init__(self, stocks: Iterable[Stock] | None = None):
        if stocks is not None:
            self.__data = {stock.symbol: stock for stock in stocks}

    def __delitem__(self, symbol: str):
        if symbol in self.__data:
            del self.__data[symbol]
        else:
            raise KeyError(f'No such stock symbol {symbol}')

    def __getitem__(self, symbol: str) -> Stock:
        if symbol in self.__data:
            return self.__data[symbol]
        else:
            raise KeyError(f'No such stock symbol {symbol}')

    def add(self, stock: Stock):
        "Add a stock to db"
        self.__data[stock.symbol] = stock

    def __iadd__(self, stock: Stock) -> "_StockDB":
        self.add(stock)
        return self

    def __iter__(self) -> Iterator:
        return iter(self.__data)

    def __len__(self) -> int:
        return len(self.__data)

    def __repr__(self):
        return f"StockDB(\n\t{'\n\t'.join(repr(stock) for stock in self.values())}\n)"

    def list(self) -> List[Stock]:
        "Get list of stocks in db"
        return list(self.__data.values())

    def symbols(self) -> List[str | None]:
        "Get symbols list"
        return list(self.__data.keys())

    def get_k_random_symbols(self, k: int = 1) -> Stock:
        "Get k random stocks"
        return choices(self.symbols(), k=k)

    @classmethod
    def create(cls, path: Union[Path, str] | None) -> "_StockDB":
        """
        Create an empty StockDB or create and populate from file
        """
        return cls(Stock.from_csv(path)) if path is not None else cls()


class StockDB:
    """
    Singleton wrapper
    """
    __instance: _StockDB | None = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = _StockDB()
        return cls.__instance

    @classmethod
    def is_initialized(cls) -> bool:
        """
        Returns true if the singleton has been initialized at least once
        """
        return cls.__instance is not None

    @classmethod
    def list(cls) -> List[Stock]:
        "Get list of stocks in db"
        return cls.__instance.list()

    @classmethod
    def symbols(cls) -> List[str | None]:
        "Get symbols list"
        return cls.__instance.symbols()

    @classmethod
    def reset(cls):
        """
        Clear and reset DB
        """
        del cls.__instance
        gc.collect()
        cls.__instance = None

    @classmethod
    def create(cls, path: Union[Path, str] | None) -> "StockDB":
        """
        Overrides create with singleton specific logic
        """
        if cls.__instance is not None:
            raise AssertionError(
                f"Class {cls.__name__} must only have 1 instance"
            )
        cls.__instance = _StockDB.create(path)
        return cls.__instance
