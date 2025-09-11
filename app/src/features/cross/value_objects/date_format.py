from enum import Enum


class DateFormat(Enum):
    """
    Enum representing different date and time formats
    """

    DATE: str = "%Y%m%d"
    TIMESTAMP: str = "%Y%m%d%H%M%S"