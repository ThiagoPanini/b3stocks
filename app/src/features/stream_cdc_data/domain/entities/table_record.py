from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class TableRecord:
    """
    Represents a table record streamed from a database through CDC.

    This entity was defined based on DynamoDB streams structure and currently may not represents
    all CDC use cases.
    """
    table_name: str
    event_id: str
    event_name: str
    event_version: str
    event_source: str
    aws_region: str
    table_keys: dict[str, Any]
    table_new_image: Optional[dict[str, Any]] = None
    table_old_image: Optional[dict[str, Any]] = None
    sequence_number: Optional[str] = None
    size_bytes: Optional[int] = None
    stream_view_type: Optional[str] = None
    event_source_arn: str = None
    event_date: str = None
