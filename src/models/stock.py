"""
    Implements a Stock model
"""

from typing import Any

from pydantic import field_validator, validator, BaseModel, Field

from src.formulas.formulas import StockScalarFormulasMixin
from src.models.stock_type import StockType
from src.parsers.csv_parser import CsvParserMixin


class Stock(BaseModel, CsvParserMixin, StockScalarFormulasMixin):
    """
    Represents a Global Beverage Corporation Exchange Stock
    """

    symbol: str = Field(pattern=r"^[A-Z]{3}$")
    type: StockType
    last_dividend: float = Field(ge=0.0)
    fixed_dividend: float | None
    par_value: float = Field(ge=0.0)

    # pylint: disable=R0903
    class Config:
        "Stock model configuration"
        frozen: bool = True
        str_strip_whitespace = True
        use_enum_values = True

    @field_validator("last_dividend", "fixed_dividend", "par_value", mode="before")
    @staticmethod
    def _strip_str(value: Any) -> Any:
        if isinstance(value, str):
            return value.strip() if len(value) else None
        return value

    @validator("type", pre=True)
    @staticmethod
    def _to_upper(value: str) -> str:
        return value.upper()

    @validator("fixed_dividend")
    @staticmethod
    def _validate_percentage(value: float | None) -> float | None:
        if value is not None and not 0 <= value <= 100:
            raise ValueError("Must be in range [0-100]")
        return value / 100 if value is not None else value

    @classmethod
    def from_fields(cls, *field_values) -> "Stock":
        """
        Create Stock object from string fields.
        Example:
            Useful to convert a row parsed from csv into a Stock object.
        """
        return cls(
            **{field: value for field, value in zip(cls.model_fields, field_values)}
        )
