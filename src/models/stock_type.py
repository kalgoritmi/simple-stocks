"""
Enum helper for stock type
"""

from enum import Enum

class StockType(str, Enum):
    """
    Enum representing stock type
    Binary, either COMMON or PREFERRED

    Attributes:
        COMMON (str)
        PREFERRED (str)
    """

    COMMON = "COMMON"
    PREFERRED = "PREFERRED"
