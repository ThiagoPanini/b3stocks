from dataclasses import dataclass
from typing import Any, Optional
from datetime import datetime


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
    event_source_service: str
    aws_region: str
    table_keys: dict[str, Any]
    table_new_image: Optional[dict[str, Any]]
    table_old_image: Optional[dict[str, Any]]
    sequence_number: Optional[str]
    size_bytes: Optional[int]
    stream_view_type: Optional[str]
    event_source_arn: str
    event_timestamp: datetime
    event_date: str
