from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class EventStreamData:
    """
    Represents a stream data in an event record.

    This entity was defined based on DynamoDB streams structure and currently may not represents
    all CDC use cases.
    """
    keys: dict[str, Any]
    new_image: Optional[dict[str, Any]] = None
    old_image: Optional[dict[str, Any]] = None
    sequence_number: Optional[str] = None
    size_bytes: Optional[int] = None
    stream_view_type: Optional[str] = None
    approx_ts: Optional[Any] = None