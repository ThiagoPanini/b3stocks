from dataclasses import dataclass
from typing import Any

from app.src.features.stream_dynamodb_data.domain.entities.dynamodb_stream_data import DynamoDBStreamData
from app.src.features.stream_dynamodb_data.domain.entities.dynamodb_event_record import DynamoDBEventRecord
from app.src.features.stream_dynamodb_data.domain.entities.dynamodb_table_record import DynamoDBTableRecord
from app.src.features.stream_dynamodb_data.domain.dtos.input_dto import DynamoDBStreamsInputDTO
from app.src.features.stream_dynamodb_data.infra.mappers.lambda_event_mapper import LambdaEventMapper


@dataclass(frozen=True)
class StreamDynamoDBDataUseCase:
    """
    Use case for streaming DynamoDB data to a storage repository.
    """

    def execute(self, input_dto: DynamoDBStreamsInputDTO) -> Any:
        """
        Executes the use case to map the AWS Lambda event to InputDTO.
        """

        # Build table records for each event record
        table_records: list[DynamoDBTableRecord] = []

        for record in input_dto.records:
            table_record = DynamoDBTableRecord(
                table_name=record.table_name,
                event_name=record.event_name,
                event_ts=record.event_ts,
                sequence_number=record.dynamodb.sequence_number,
                keys=record.dynamodb.keys,
                new_image=record.dynamodb.new_image,
                old_image=record.dynamodb.old_image,
                source_region=record.aws_region,
                is_deleted=record.event_name == "REMOVE",
                event_date=record.event_date
            )

            table_records.append(table_record)

        return table_records

"""
ToDos:
    - Build a repository interface to handle the storage of the table records.
    - Implement the repository interface to store records in the desired storage solution (e.g., S3, another DynamoDB table).
    - Study the best way to use awswrangler to sync with glue data catalog
"""