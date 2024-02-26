"""
Enum helper for stock type
"""

from enum import Enum

class StockType(str, Enum):
    """
    Enum representing stock type
    Binary, either COMMON or PREFERRED
    """

    COMMON = "COMMON"
    PREFERRED = "PREFERRED"
