from dataclasses import dataclass
from typing import Any, Optional

@dataclass
class OutputDTO:
    """
    A generic result wrapper for use case execution.

    This class represents the outcome of a use case execution and should be used
    to encapsulate either a successful result or a failure with an error message.

    Args:
        success (bool): Indicates whether the execution was successful.
        data (Optional[Any]): The result data returned when the execution is successful.
        error (Optional[str]): The error message returned when the execution fails.
    """

    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None


    @classmethod
    def ok(cls, data: Any = None) -> "OutputDTO":
        """
        Create a successful OutputDTO instance.

        Args:
            data (Any): The data to be returned in the successful response.
        """
        return cls(success=True, data=data)


    @classmethod
    def fail(cls, error: str) -> "OutputDTO":
        """
        Create a failed OutputDTO instance.

        Args:
            error (str): The error message to be returned in the failed response.
        """
        return cls(success=False, error=error)


    def to_dict(self) -> dict:
        """
        Convert the OutputDTO instance to a dictionary.

        Returns:
            dict: A dictionary representation of the OutputDTO instance.
        """
        return {
            "success": self.success,
            "data": self.data,
            "error": self.error
        }