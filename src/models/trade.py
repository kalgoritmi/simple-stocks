"""
Stock Trade model 
"""
from datetime import datetime
from enum import Enum
from random import choices

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
    def get_k_random_indicators(cls, k: int = 1) -> str:
        "Get k random indicators"
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
        if value not in StockDB.symbols():
            raise ValueError(f'Invalid stock symbol {value}')
        return value

    def get_stock(self) -> Stock:
        "Get stock from symbol reference"
        # pylint: disable=E1136
        return StockDB()[self.symbol]

    @classmethod
    def from_fields(cls, *field_values) -> "Trade":
        """
        Create Trade object from string fields.
        Example:
            Useful to convert a row parsed from csv into a Trade object.
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
        """
        return cls(
            timestamp=mock_timestamp or datetime.now(),
            symbol=trade.symbol,
            price=trade.price,
            quantity=trade.quantity,
            indicator=trade.indicator
        )
