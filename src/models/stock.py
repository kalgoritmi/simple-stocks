"""
    Implements a Stock model
"""

from typing import Any, Tuple

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
        "Strip whitespace if not None otherwise forward"
        if isinstance(value, str):
            return value.strip() if len(value) else None
        return value

    @validator("type", pre=True)
    @staticmethod
    def _to_upper(value: str) -> str:
        "Convert str to upper case"
        return value.upper()

    @validator("fixed_dividend")
    @staticmethod
    def _validate_percentage(value: float | None) -> float | None:
        """
        Validate field to be a percentage value
        
        Attributes:
            value (float | None): the value to be validated
            expects a float representing a percentage e.g. 2.5%
            then converts it to a float by dividing with 100
        
        Returns:
            validated value (float | None)
        """
        if value is not None and not 0 <= value <= 100:
            raise ValueError("Must be in range [0-100]")
        return value / 100 if value is not None else value

    @classmethod
    def from_fields(cls, *field_values: Tuple[Any]) -> "Stock":
        """
        Create Stock object from string fields.
        
        Useful to convert a row parsed from csv into a Stock object,
        due to pydantic enforcing keyword arguments.

        This factory proivides an easy way to instantiate using
        positional arguments
        
        Attributes:
            cls (Stock type)
            *field_values (Tuple[Any]): a tuple holding the fields used to
                instatiate the model
        
        Returns:
            instantiated stock object (Stock)
        """
        return cls(
            **{field: value for field, value in zip(cls.model_fields, field_values)}
        )
