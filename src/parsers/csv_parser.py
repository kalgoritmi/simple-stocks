"""
CSV stock parsing utility module
"""

from csv import reader
from pathlib import Path
from typing import Generator


# pylint: disable=R0903
class CsvParserMixin:
    """
    Mix-in class implements parsing from csv for a model class.
    """

    @classmethod
    def from_csv(cls, csv_path: Path | str) -> Generator:
        """
        Method that gets mixed in to target class.

        Requires the `from_fields` class method interface to build a target object
        for each row and yields from a generator expression.

        Attributes:
            cls (StockDB | TradeDB): expects the interface of either stock or trade db
            csv_path (Path | str): a pathlib object or an str to the csv file
        
        Raises:
            FileNotFoundError: if the file can not be found
            AttributeError: if no from_fields factory is implemented

        Returns:
            Generator object of eitther StockDB or TradeDB
        """
        if isinstance(csv_path, str):
            csv_path = Path(csv_path)

        if not csv_path.exists():
            raise FileNotFoundError(f"File {csv_path.resolve()} does not exist")

        if not hasattr(cls, _fn := "from_fields"):
            raise AttributeError(f"Classmethod {_fn} needs to be implemented")

        with open(csv_path, encoding="utf-8") as csv_file:
            csv_it = reader(csv_file)
            next(csv_it)  # pylint: disable=R1708
            yield from (cls.from_fields(*row) for row in csv_it)
