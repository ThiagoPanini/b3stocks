from dataclasses import dataclass
from typing import Any, Optional
from datetime import datetime


@dataclass
class DynamoDBStreamsOutputData:
    """
    Represents the output data that will be sent to the target system as part of the stream process.

    The attributes defined in this entity class will match the output schema required by the target
    system (e.g. a table in the Glue Data Catalog).
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
