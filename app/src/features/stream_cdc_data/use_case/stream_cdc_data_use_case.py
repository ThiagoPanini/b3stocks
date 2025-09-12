from dataclasses import dataclass
from typing import Any
from datetime import datetime, timezone
import re

from app.src.features.cross.utils.log_utils import setup_logger
from app.src.features.stream_cdc_data.domain.dtos.input_dto import StreamCDCDataInputDTO
from app.src.features.stream_cdc_data.domain.entities.table_record import TableRecord
from app.src.features.cross.value_objects import DateFormat
from app.src.features.cross.domain.dtos.output_dto import OutputDTO

logger = setup_logger(name=__name__)


@dataclass(frozen=True)
class StreamCDCDataUseCase:
    """
    Use case for streaming CDC data to a storage repository.
    """

    def __transform_event_date(self, approx_ts: Any) -> str:
        """
        Transforms the ApproximateCreationDateTime from a database stream record to ISO 8601 string.

        Args:
            approx_ts (Any): The ApproximateCreationDateTime value from a database stream record.

        Returns:
            str: The event date in ISO 8601 format.
        """
        if isinstance(approx_ts, (int, float)):
            event_date = datetime.fromtimestamp(approx_ts, tz=timezone.utc)
        else:
            event_date = datetime.now(tz=timezone.utc)

        return event_date.strftime(DateFormat.DATE.value)


    def __get_table_name_from_source_arn(self, source_arn: str) -> str:
        """
        Extracts the table name from the event source ARN using regular expression.

        Args:
            source_arn (str): The event source ARN.
        """
        try:
            # ARN format: arn:aws:<db_service>:region:account-id:table/TableName/stream/timestamp
            match = re.search(r"table\/(.+?)\/stream", source_arn)
            return match.group(1) if match else "unknown-table"

        except (IndexError, AttributeError):
            return "unknown-table"  # Fallback if parsing fails


    def execute(self, input_dto: StreamCDCDataInputDTO) -> OutputDTO:
        """
        Executes the use case to map the AWS Lambda event to InputDTO.

        Args:
            input_dto (StreamCDCDataInputDTO): The input DTO containing event records.
        
        Returns:
            OutputDTO: The output DTO containing the list of table records.
        """

        # Build table records for each event record
        table_records: list[TableRecord] = []

        for record in input_dto.records:
            try:
                table_record = TableRecord(
                    table_name=self.__get_table_name_from_source_arn(record.event_source_arn),
                    event_id=record.event_id,
                    event_name=record.event_name,
                    event_version=record.event_version,
                    event_source=record.event_source,
                    aws_region=record.aws_region,
                    table_keys=record.event_stream_data.keys,
                    table_new_image=record.event_stream_data.new_image,
                    table_old_image=record.event_stream_data.old_image,
                    sequence_number=record.event_stream_data.sequence_number,
                    size_bytes=record.event_stream_data.size_bytes,
                    stream_view_type=record.event_stream_data.stream_view_type,
                    event_source_arn=record.event_source_arn,
                    event_date=self.__transform_event_date(approx_ts=record.event_stream_data.approx_ts)
                )

                table_records.append(table_record)
            
            except Exception:
                logger.exception(f"Error processing record with event ID {record.event_id}")
                raise
        
        print(table_records)

        return OutputDTO.ok(
            data={
                "total_table_records": len(table_records)
            }
        )

"""
ToDos:
    CDC:
        Adds attributes on entities that represents the database service, output bucket location, and others
"""