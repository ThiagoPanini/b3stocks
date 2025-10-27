from dataclasses import dataclass

from app.src.features.store_dynamodb_streams_data.domain.entities.dynamodb_streams_event_record import (
    DynamoDBStreamsEventRecord
)


@dataclass
class DynamoDBStreamsInputDTO:
    """
    Data Transfer Object for input data from DynamoDB Streams.
    """
    records: list[DynamoDBStreamsEventRecord]