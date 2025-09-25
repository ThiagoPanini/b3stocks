from enum import Enum


class DateFormat(Enum):
    """
    Enum representing different date and time formats
    """

    DATE: str = "%Y-%m-%d"
    DATE_AND_TIME: str = "%Y-%m-%d %H:%M:%S"
    DATE_AND_TIME_WITH_TZ: str = "%Y-%m-%d %H:%M:%S%z"
    