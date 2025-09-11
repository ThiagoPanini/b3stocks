from typing import Any
from decimal import Decimal
from datetime import datetime, timezone

from boto3.dynamodb.types import TypeDeserializer

from app.src.features.stream_dynamodb_data.domain.entities.dynamodb_stream_data import DynamoDBStreamData
from app.src.features.stream_dynamodb_data.domain.entities.dynamodb_event_record import DynamoDBEventRecord
from app.src.features.stream_dynamodb_data.domain.dtos.input_dto import DynamoDBStreamsInputDTO

from app.src.features.cross.value_objects import DateFormat


class LambdaEventMapper:
    """
    Maps AWS Lambda event dict to InputDTO class.
    """
    
    def __init__(self):
        self.__deserializer = TypeDeserializer()


    def __convert_values_on_dynamodb_stream_record(self, value: Any) -> dict[str, Any]:
        """
        Converts a DynamoDB stream record value (already TypeDeserialized) into plain
        JSON-serializable dict.

        Args:
            value (dict[str, Any]): The value in a DynamoDB stream record to convert.
        """
        # If value is a list, then convert each item in the list
        if isinstance(value, list):
            return [self.__convert_values_on_dynamodb_stream_record(v) for v in value]
        # If value is a set, convert to list and then convert each item in the list
        if isinstance(value, set):
            return [self.__convert_values_on_dynamodb_stream_record(v) for v in list(value)]
        # If value is a dict, convert each key-value pair in the dict
        if isinstance(value, dict):
            return {k: self.__convert_values_on_dynamodb_stream_record(v) for k, v in value.items()}
        # If value is a Decimal, convert to int or float
        if isinstance(value, Decimal):
            # Attempt int if no fractional part else float
            if value % 1 == 0:
                return int(value)
            return float(value)

        return value


    def __deserialize_dynamodb_stream_record(self, stream_record: dict[str, Any]) -> dict[str, Any]:
        """
        Deserializes a DynamoDB stream record using boto3 TypeDeserializer.

        Args:
            stream_record (dict[str, Any]): The DynamoDB stream record to deserialize.
        """
        deserialized_stream_record = {
            k: self.__deserializer.deserialize(v) for k, v in stream_record.items()
        }

        return self.__convert_values_on_dynamodb_stream_record(value=deserialized_stream_record)


    def __transform_event_date(self, approx_ts: Any) -> str:
        """
        Transforms the ApproximateCreationDateTime from DynamoDB stream record to ISO 8601 string.

        Args:
            approx_ts (Any): The ApproximateCreationDateTime value from DynamoDB stream record.
        """
        if isinstance(approx_ts, (int, float)):
            event_dt = datetime.fromtimestamp(approx_ts, tz=timezone.utc)
        else:
            event_dt = datetime.now(tz=timezone.utc)

        return event_dt


    def __get_table_name_from_source_arn(self, source_arn: str) -> str:
        """
        Extracts the table name from the event source ARN.

        Args:
            source_arn (str): The event source ARN.
        """
        try:
            # ARN format: arn:aws:dynamodb:region:account-id:table/TableName/stream/timestamp
            return source_arn.split(":")[-1].split("/")[1]
        except (IndexError, AttributeError):
            return "unknown-table"  # Fallback if parsing fails


    def map_event_to_input_dto(self, event: dict[str, Any]) -> DynamoDBStreamsInputDTO:
        """
        Maps AWS Lambda event dict to InputDTO class.

        Args:
            event (dict[str, Any]): The AWS Lambda event dict.
        """
        records = event.get("Records", [])
        if not records:
            raise ValueError("No records found in source event")

        # Iterating over each record and mapping to entities
        dynamodb_event_records: list[DynamoDBEventRecord] = []
        for record in records:
            # Getting dynamodb data from record
            dynamodb_data = record.get("dynamodb", {})
            keys = dynamodb_data.get("Keys", {})
            new_image = dynamodb_data.get("NewImage", {})
            old_image = dynamodb_data.get("OldImage", {})
            approx_ts = dynamodb_data.get("ApproximateCreationDateTime")

            # Transforming dynamodb stream data fields
            deserialized_keys = self.__deserialize_dynamodb_stream_record(keys)
            deserialized_new_image = self.__deserialize_dynamodb_stream_record(new_image) if new_image else None
            deserialized_old_image = self.__deserialize_dynamodb_stream_record(old_image) if old_image else None
            event_date = self.__transform_event_date(approx_ts=approx_ts)
            table_name = self.__get_table_name_from_source_arn(record.get("eventSourceARN", ""))

            # Creating DynamoDBStreamData entity
            dynamodb_stream_data = DynamoDBStreamData(
                keys=deserialized_keys,
                new_image=deserialized_new_image,
                old_image=deserialized_old_image,
                sequence_number=dynamodb_data.get("SequenceNumber"),
                size_bytes=dynamodb_data.get("SizeBytes"),
                stream_view_type=dynamodb_data.get("StreamViewType"),
            )

            # Creating DynamoDBEventRecord entity
            dynamodb_event_record = DynamoDBEventRecord(
                event_id=record.get("eventID", ""),
                event_name=record.get("eventName", ""),
                event_version=record.get("eventVersion", ""),
                event_source=record.get("eventSource", ""),
                aws_region=record.get("awsRegion", ""),
                dynamodb=dynamodb_stream_data,
                event_source_arn=record.get("eventSourceARN", ""),
                table_name=table_name,
                event_ts=event_date.isoformat(),
                event_date=event_date.strftime(DateFormat.DATE.value)
            )
            dynamodb_event_records.append(dynamodb_event_record)

        return DynamoDBStreamsInputDTO(records=dynamodb_event_records)
