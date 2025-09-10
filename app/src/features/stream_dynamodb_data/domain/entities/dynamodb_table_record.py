from dataclasses import dataclass
from typing import Any


@dataclass
class DynamoDBTableRecord:
    """
    Represents a DynamoDB table record to be streamed to a storage repository.
    """
    table_name: str
    event_name: str
    event_ts: str
    sequence_number: str
    keys: dict[str, Any]
    new_image: dict[str, Any]
    old_image: dict[str, Any]
    source_region: str
    is_deleted: bool
    event_date: str