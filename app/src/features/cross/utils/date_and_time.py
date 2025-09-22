from datetime import datetime

from app.src.features.cross.value_objects import (
    Timezone,
    DateFormat
)


class DateAndTimeUtils:
    """
    Utility class for handling date and time generation handling timezone.
    """
    
    @staticmethod
    def datetime_now(timezone: Timezone) -> datetime:
        """
        Returns the current datetime in the specified timezone.
        
        Args:
            timezone (Timezone): The timezone to use for the current datetime.
        
        Returns:
            datetime: Current datetime in the specified timezone
        """
        return datetime.now(timezone.value)


    @staticmethod
    def utc_to_timezone(utc_datetime: datetime, timezone: Timezone) -> datetime:
        """
        Converts a UTC datetime to a timezone.
        
        Args:
            utc_datetime (datetime): UTC datetime object
            timezone (Timezone): The target timezone to convert to

        Returns:
            datetime: Datetime converted to the target timezone
        """
        return utc_datetime.astimezone(timezone.value)


    @staticmethod
    def from_timestamp(unix_ts: float, timezone: Timezone) -> datetime:
        """
        Creates a datetime object from a Unix timestamp in the specified timezone.

        Args:
            unix_ts (float): Unix timestamp
            timezone (Timezone): The timezone to use for the datetime object

        Returns:
            datetime: Datetime object in the specified timezone
        """
        return datetime.fromtimestamp(unix_ts, tz=timezone.value)


    @staticmethod
    def datetime_to_str(dt: datetime, format: DateFormat) -> str:
        """
        Converts a datetime object to a string based on the provided format.

        Args:
            dt (datetime): The datetime object to format
            format (DateFormat): The format string to use for formatting

        Returns:
            str: Formatted date/time string
        """
        return dt.strftime(format.value)


    @staticmethod
    def datetime_now_str(timezone: Timezone, format: DateFormat) -> str:
        """
        Returns the current datetime in the specified timezone in a string format.
        
        Args:
            timezone (Timezone): The timezone to use for the current datetime.
            format (DateFormat): The format string to use for formatting.

        Returns:
            str: Formatted date/time string
        """
        return DateAndTimeUtils.datetime_to_str(
            dt=DateAndTimeUtils.datetime_now(timezone=timezone),
            format=format
        )
