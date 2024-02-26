"""
Stock Trade model 
"""
from datetime import datetime
from enum import Enum
from random import choices
from typing import Any, List, Tuple

from pydantic import BaseModel, PositiveFloat, PositiveInt, validator

from src.db.stock_db import StockDB
from src.models.stock import Stock
from src.parsers.csv_parser import CsvParserMixin

class TransactionIndicator(str, Enum):
    """
    Enum represting the transaction type for a given shares trade
    """
    BUY = "BUY"
    SELL = "SELL"

    @classmethod
    def get_k_random_indicators(cls, k: int = 1) -> List[str]:
        """
        Get k random indicators
        
        Attributes:
            cls: the type
            k (int, default: 1): the number of indicators to return

        Returns:
            a list of k indicators that are either BUY or SELL (List[str])
        """
        return choices([cls.BUY, cls.SELL], k=k)


class Trade(BaseModel, CsvParserMixin):
    """
    Represents a trade transaction
    """
    symbol: str
    price: PositiveFloat
    quantity: PositiveInt
    indicator: TransactionIndicator

    # pylint: disable=R0903
    class Config:
        "Trade model configuration"
        frozen: bool = True
        str_strip_whitespace = True
        use_enum_values = True

    if not StockDB.is_initialized():
        raise AssertionError(
            f'Class requires initialization of {StockDB.__name__}'
        )

    @validator('symbol', pre=True)
    @staticmethod
    def _validate_stock_symbol(value: str):
        "Checks if symbol is in StockDB "
        if value not in StockDB.symbols():
            raise ValueError(f'Invalid stock symbol {value}')
        return value

    def get_stock(self) -> Stock:
        "Get stock from symbol reference"
        # pylint: disable=E1136
        return StockDB()[self.symbol]

    @classmethod
    def from_fields(cls, *field_values: Tuple[Any]) -> "Trade":
        """
        Create Trade object from string fields.
        
        Useful to convert a row parsed from csv into a Trade object,
        due to pydantic enforcing keyword arguments.

        This factory proivides an easy way to instantiate using
        positional arguments
        
        Attributes:
            cls (Trade type)
            *field_values (Tuple[Any]): a tuple holding the fields used to
                instatiate the model
        
        Returns:
            instantiated trade object (Trade)
        """
        return cls(
            **{field: value for field, value in zip(cls.model_fields, field_values)}
        )

class TradeWithTimestamp(Trade):
    """
    Trade with timestamp
    """
    timestamp: datetime

    @classmethod
    def from_trade(
        cls,
        trade: Trade,
        mock_timestamp: datetime | None = None
    ) -> "TradeWithTimestamp":
        """
        Augment Trade with timestamp

        Attributes:
            cls
            trade (Trade): an instantiated trade object to init from
            mock_timestamp (datetime | None): a mock timestamp to insert
                if not given the current timestamp is taken into account
        """
        return cls(
            timestamp=mock_timestamp or datetime.now(),
            symbol=trade.symbol,
            price=trade.price,
            quantity=trade.quantity,
            indicator=trade.indicator
        )
