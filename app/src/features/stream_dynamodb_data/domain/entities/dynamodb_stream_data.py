from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class DynamoDBStreamData:
    """
    Represents a DynamoDB stream data in an event record.
    """
    keys: dict[str, Any]
    new_image: Optional[dict[str, Any]] = None
    old_image: Optional[dict[str, Any]] = None
    sequence_number: Optional[str] = None
    size_bytes: Optional[int] = None
    stream_view_type: Optional[str] = None