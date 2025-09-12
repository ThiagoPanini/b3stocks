from dataclasses import dataclass
from datetime import datetime

from app.src.features.stream_cdc_data.domain.entities.event_stream_data import EventStreamData


@dataclass
class EventRecord:
    """
    Represents an event record streamed from a database.

    This entity was defined based on DynamoDB streams structure and currently may not represents
    all CDC use cases.
    """
    event_id: str
    event_name: str
    event_version: str
    event_source: str
    aws_region: str
    event_stream_data: EventStreamData
    event_source_arn: str
