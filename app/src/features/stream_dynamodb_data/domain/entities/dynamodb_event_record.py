from dataclasses import dataclass
from datetime import datetime

from app.src.features.stream_dynamodb_data.domain.entities.dynamodb_stream_data import DynamoDBStreamData


@dataclass
class DynamoDBEventRecord:
    """
    Represents a DynamoDB event record.
    """
    event_id: str
    event_name: str
    event_version: str
    event_source: str
    aws_region: str
    dynamodb: DynamoDBStreamData
    event_source_arn: str
    table_name: str
    event_ts: str
    event_date: datetime
