import json
from dataclasses import asdict, is_dataclass
from enum import Enum
from typing import Any, Optional
from datetime import datetime

from app.src.features.cross.domain.dtos.output_dto import OutputDTO


class HTTPResponseMapper:
    """
    Maps OutputDTO results to HTTP responses for the presentation layer.
    """

    DEFAULT_HEADERS = {
        "Content-Type": "application/json"
    }

    @staticmethod
    def map(
        output_dto: OutputDTO,
        headers: Optional[dict[str, str]] = DEFAULT_HEADERS
    ) -> dict[str, Any]:
        """
        Maps the output DTO to an HTTP response format.

        Args:
            output_dto (OutputDTO): The output DTO containing the data to be returned.
            headers (Optional[dict[str, str]]): Optional headers for the HTTP response.

        Returns:
            dict[str, Any]: A dictionary representing the HTTP response.
        """

        # Determine status code
        if output_dto.success:
            status_code = 200
        elif output_dto.error:
            # Custom error mapping
            error_msg = output_dto.error.lower()
            if "not found" in error_msg:
                status_code = 404
            elif "unauthorized" in error_msg:
                status_code = 401
            elif "forbidden" in error_msg:
                status_code = 403
            elif "conflict" in error_msg:
                status_code = 409
            elif "bad request" in error_msg:
                status_code = 400
            elif "internal" in error_msg or "exception" in error_msg:
                status_code = 500
            else:
                status_code = 400
        else:
            status_code = 400

        body = json.dumps(output_dto.to_dict(), default=HTTPResponseMapper._json_default)
        return {
            "statusCode": status_code,
            "headers": headers,
            "body": body
        }

    @staticmethod
    def _json_default(obj: Any) -> Any:
        """
        Best-effort conversion of complex objects to JSON-serializable types.

        Rules:
        - dataclasses -> dict via asdict
        - Enums -> their value
        - objects with to_dict -> call it
        - sets/tuples -> list
        - bytes -> utf-8 string (fallback to latin-1)
        - datetime -> ISO 8601 string
        """
        if is_dataclass(obj):
            return asdict(obj)
        if isinstance(obj, Enum):
            return obj.value
        to_dict = getattr(obj, "to_dict", None)
        if callable(to_dict):
            return to_dict()
        if isinstance(obj, (set, tuple)):
            return list(obj)
        if isinstance(obj, (bytes, bytearray)):
            try:
                return obj.decode("utf-8")
            except Exception:
                return obj.decode("latin-1", errors="replace")
        if isinstance(obj, datetime):
            return obj.isoformat()
        # Let json raise a TypeError for anything else
        raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")
