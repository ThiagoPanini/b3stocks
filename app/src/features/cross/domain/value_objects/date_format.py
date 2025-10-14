from enum import Enum


class DateFormat(Enum):
    """
    Enum representing different date and time formats
    """
    DATE = "%Y-%m-%d"
    DATE_AND_TIME = "%Y-%m-%d %H:%M:%S"
    DATE_AND_TIME_WITH_TZ = "%Y-%m-%d %H:%M:%S%z"
