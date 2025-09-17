from dataclasses import dataclass

from app.src.features.cross.domain.entities.dynamodb_streams_record_data import DynamoDBStreamsRecordData


@dataclass
class DynamoDBStreamsEventRecord:
    """
    Represents an event record streamed from a DynamoDB database.
    """
    event_id: str
    event_name: str
    event_version: str
    event_source: str
    aws_region: str
    record_data: DynamoDBStreamsRecordData
    event_source_arn: str
