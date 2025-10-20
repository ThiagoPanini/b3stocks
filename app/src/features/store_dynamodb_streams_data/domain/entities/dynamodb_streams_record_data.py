from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class DynamoDBStreamsRecordData:
    """
    Represents the record data in a DynamoDB Streams event record.
    """
    keys: dict[str, Any]
    new_image: Optional[dict[str, Any]]
    old_image: Optional[dict[str, Any]]
    sequence_number: Optional[str]
    size_bytes: Optional[int]
    stream_view_type: Optional[str]
    approx_ts: Optional[int | float]