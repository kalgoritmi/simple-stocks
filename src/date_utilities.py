"""
Date utilities
"""

from datetime import datetime, timedelta

from pydantic import PositiveInt

def timestamp_n_minutes_ago(
    n: PositiveInt = 15,
    mock_ts: datetime | None = None
) -> datetime:
    """
    Timestamp n minutes ago
    
    Attributes:
        n (PositiveInt, default: 15): the number of minutes to substract from timestamp
        mock_ts (datetime | None): if given sets the init timestamp to the mock otherwise gets the timestamp of present moment
    
    Returns:
        returns the difference of timestamp and n minutes (datetime)
    """
    if mock_ts is None:
        return datetime.now() - timedelta(minutes=n)
    return mock_ts - timedelta(minutes=n)
