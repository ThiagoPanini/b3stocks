from typing import Any
from decimal import Decimal

from boto3.dynamodb.types import TypeDeserializer

from app.src.features.cross.domain.entities.dynamodb_streams_record_data import DynamoDBStreamsRecordData
from app.src.features.cross.domain.entities.dynamodb_streams_event_record import DynamoDBStreamsEventRecord
from app.src.features.cross.domain.dtos.dynamodb_streams_input_dto import DynamoDBStreamsInputDTO
from app.src.features.cross.utils.serialization import json_serialize

from app.src.features.cross.value_objects import DateFormat


class DynamoDBStreamsLambdaEventMapper:
    """
    Maps a DynamoDB Streams Lambda event dict to a input Data Transfer Object (DTO) class
    """
    
    def __init__(self):
        self.__deserializer = TypeDeserializer()


    def __deserialize_stream_record(self, stream_record: dict[str, Any]) -> dict[str, Any]:
        """
        Deserializes a database stream record using boto3 TypeDeserializer.

        This method was based on DynamoDB streams structure and currently may not represents
        all CDC use cases.

        Args:
            stream_record (dict[str, Any]): The database stream record to deserialize.
        """
        deserialized_stream_record = {
            k: self.__deserializer.deserialize(v) for k, v in stream_record.items()
        }

        return json_serialize(deserialized_stream_record)


    def map_event_to_input_dto(self, event: dict[str, Any]) -> DynamoDBStreamsInputDTO:
        """
        Maps a DynamoDB Streams Lambda event dict to a input Data Transfer Object (DTO) class

        Args:
            event (dict[str, Any]): The AWS Lambda event dict received from DynamoDB Streams.
            database_service (str): The database service name in the event dict. Default is "dynamodb".
        """
        records = event.get("Records", [])
        if not records:
            raise ValueError("No records found in source event")

        # Iterating over each record and mapping to entities
        event_records: list[DynamoDBStreamsEventRecord] = []
        for record in records:
            # Getting record data from event
            record_data_raw = record.get("dynamodb", {})

            # Getting keys and images data
            keys = record_data_raw.get("Keys", {})
            new_image = record_data_raw.get("NewImage", {})
            old_image = record_data_raw.get("OldImage", {})

            # Deserializing keys and images
            deserialized_keys = self.__deserialize_stream_record(keys)
            deserialized_new_image = self.__deserialize_stream_record(new_image)
            deserialized_old_image = self.__deserialize_stream_record(old_image)

            # Creating DynamoDBStreamsRecordData entity
            record_data = DynamoDBStreamsRecordData(
                keys=deserialized_keys,
                new_image=deserialized_new_image,
                old_image=deserialized_old_image,
                sequence_number=record_data_raw.get("SequenceNumber"),
                size_bytes=record_data_raw.get("SizeBytes"),
                stream_view_type=record_data_raw.get("StreamViewType"),
                approx_ts=record_data_raw.get("ApproximateCreationDateTime")
            )

            # Creating EventRecord entity
            event_record = DynamoDBStreamsEventRecord(
                event_id=record.get("eventID", ""),
                event_name=record.get("eventName", ""),
                event_version=record.get("eventVersion", ""),
                event_source=record.get("eventSource", ""),
                aws_region=record.get("awsRegion", ""),
                record_data=record_data,
                event_source_arn=record.get("eventSourceARN", "")
            )
            event_records.append(event_record)

        return DynamoDBStreamsInputDTO(records=event_records)
