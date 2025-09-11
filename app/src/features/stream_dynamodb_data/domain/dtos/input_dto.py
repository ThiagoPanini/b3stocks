from dataclasses import dataclass
from typing import Any

from app.src.features.stream_dynamodb_data.domain.entities.dynamodb_stream_data import DynamoDBStreamData
from app.src.features.stream_dynamodb_data.domain.entities.dynamodb_event_record import DynamoDBEventRecord


@dataclass
class DynamoDBStreamsInputDTO:
    """
    Data Transfer Object for input data from AWS Lambda event.
    """
    records: list[DynamoDBEventRecord]