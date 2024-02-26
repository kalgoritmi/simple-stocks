"""
Date utilities
"""

from datetime import datetime, timedelta

from pydantic import PositiveInt

def timestamp_n_minutes_ago(
    n: PositiveInt = 15,
    mock_ts: datetime | None = None
) -> datetime:
    "Timestamp n minutes ago"
    if mock_ts is None:
        return datetime.now() - timedelta(minutes=n)
    return mock_ts - timedelta(minutes=n)
