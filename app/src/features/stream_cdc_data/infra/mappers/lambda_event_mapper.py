from typing import Any
from decimal import Decimal

from boto3.dynamodb.types import TypeDeserializer

from app.src.features.stream_cdc_data.domain.entities.event_stream_data import EventStreamData
from app.src.features.stream_cdc_data.domain.entities.event_record import EventRecord
from app.src.features.stream_cdc_data.domain.dtos.input_dto import StreamCDCDataInputDTO

from app.src.features.cross.value_objects import DateFormat


class LambdaEventMapper:
    """
    Maps AWS Lambda event dict to InputDTO class.
    """
    
    def __init__(self):
        self.__deserializer = TypeDeserializer()


    def __convert_values_on_stream_record(self, value: Any) -> dict[str, Any]:
        """
        Converts a stream record value (already TypeDeserialized) into plain
        JSON-serializable dict.

        This method was based on DynamoDB streams structure and currently may not represents
        all CDC use cases.

        Args:
            value (dict[str, Any]): The value in a database stream record to convert.
        """
        # If value is a list, then convert each item in the list
        if isinstance(value, list):
            return [self.__convert_values_on_stream_record(v) for v in value]
        # If value is a set, convert to list and then convert each item in the list
        if isinstance(value, set):
            return [self.__convert_values_on_stream_record(v) for v in list(value)]
        # If value is a dict, convert each key-value pair in the dict
        if isinstance(value, dict):
            return {k: self.__convert_values_on_stream_record(v) for k, v in value.items()}
        # If value is a Decimal, convert to int or float
        if isinstance(value, Decimal):
            # Attempt int if no fractional part else float
            if value % 1 == 0:
                return int(value)
            return float(value)

        return value


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

        return self.__convert_values_on_stream_record(value=deserialized_stream_record)


    def map_event_to_input_dto(
        self,
        event: dict[str, Any],
        database_service: str = "dynamodb"
    ) -> StreamCDCDataInputDTO:
        """
        Maps AWS Lambda event dict to InputDTO class.

        Args:
            event (dict[str, Any]): The AWS Lambda event dict.
        """
        records = event.get("Records", [])
        if not records:
            raise ValueError("No records found in source event")

        # Iterating over each record and mapping to entities
        event_records: list[EventRecord] = []
        for record in records:
            # Getting database data from record
            database_service_data = record.get(database_service, {})

            # Getting keys and images data
            keys = database_service_data.get("Keys", {})
            new_image = database_service_data.get("NewImage", {})
            old_image = database_service_data.get("OldImage", {})

            # Deserializing keys and images
            deserialized_keys = self.__deserialize_stream_record(keys)
            deserialized_new_image = self.__deserialize_stream_record(new_image)
            deserialized_old_image = self.__deserialize_stream_record(old_image)

            # Creating EventStreamData entity
            event_stream_data = EventStreamData(
                keys=deserialized_keys,
                new_image=deserialized_new_image,
                old_image=deserialized_old_image,
                sequence_number=database_service_data.get("SequenceNumber"),
                size_bytes=database_service_data.get("SizeBytes"),
                stream_view_type=database_service_data.get("StreamViewType"),
                approx_ts=database_service_data.get("ApproximateCreationDateTime")
            )

            # Creating EventRecord entity
            event_record = EventRecord(
                event_id=record.get("eventID", ""),
                event_name=record.get("eventName", ""),
                event_version=record.get("eventVersion", ""),
                event_source=record.get("eventSource", ""),
                aws_region=record.get("awsRegion", ""),
                event_stream_data=event_stream_data,
                event_source_arn=record.get("eventSourceARN", "")
            )
            event_records.append(event_record)

        return StreamCDCDataInputDTO(records=event_records)
