from dataclasses import dataclass
from datetime import datetime, UTC
import re

from app.src.features.cross.domain.dtos.dynamodb_streams_input_dto import DynamoDBStreamsInputDTO
from app.src.features.cross.domain.entities.dynamodb_streams_output_data import DynamoDBStreamsOutputData
from app.src.features.cross.domain.interfaces.cdc_data_catalog_sync_adapter_interface import (
    ICDCDataCatalogSyncAdapter
)
from app.src.features.cross.domain.dtos.output_dto import OutputDTO
from app.src.features.cross.utils.log import LogUtils
from app.src.features.cross.utils.date_and_time import DateAndTimeUtils
from app.src.features.cross.domain.value_objects import Timezone
from app.src.features.cross.domain.value_objects import DateFormat


logger = LogUtils.setup_logger(name=__name__)


@dataclass(frozen=True)
class StoreDynamoDBStreamsDataUseCase:
    """
    Use case for streaming CDC data to a storage repository.
    """

    cdc_data_catalog_sync_adapter: ICDCDataCatalogSyncAdapter


    def __get_event_timestamp(self, approx_ts: int | float) -> datetime:
        """
        Transforms the ApproximateCreationDateTime from a database stream record to a datetime format.
        Returns the timestamp in São Paulo timezone.

        Args:
            approx_ts (int | float): The ApproximateCreationDateTime value from a database stream record.

        Returns:
            datetime: The event timestamp in São Paulo timezone.
        """
        event_timestamp: datetime = DateAndTimeUtils.from_timestamp(
            unix_ts=approx_ts,
            timezone=Timezone.SAO_PAULO
        )
        return event_timestamp


    def __get_event_date(self, approx_ts: int | float) -> str:
        """
        Transforms the ApproximateCreationDateTime from a database stream record to a string date format
        in São Paulo timezone.

        Args:
            approx_ts (int | float): The ApproximateCreationDateTime value from a database stream record.

        Returns:
            str: The event date in São Paulo timezone formatted as string.
        """
        event_timestamp: datetime = self.__get_event_timestamp(approx_ts=approx_ts)
        event_date: str = DateAndTimeUtils.datetime_to_str(dt=event_timestamp, format=DateFormat.DATE)
        return event_date


    def __get_table_name_from_source_arn(self, source_arn: str) -> str:
        """
        Extracts the table name from the event source ARN using regular expression.

        Args:
            source_arn (str): The event source ARN.
        """
        try:
            # ARN format: arn:aws:<db_service>:region:account-id:table/TableName/stream/timestamp
            match = re.search(r"table\/(.+?)\/stream", source_arn)
            return match.group(1)

        except (IndexError, AttributeError):
            return "unknown-table"  # Fallback if parsing fails


    def __get_event_source_service(self, event_source: str) -> str:
        """
        Extracts the event source service from the event source string.

        Args:
            event_source (str): The event source string.
        """
        try:
            # Event source format: aws:dynamodb / Output: dynamodb
            match = re.search(r"^aws:([^:]+)", event_source)
            return match.group(1)

        except (IndexError, AttributeError):
            return event_source.split(":")[-1]  # Fallback if parsing fails


    def execute(self, input_dto: DynamoDBStreamsInputDTO) -> OutputDTO:
        """
        Executes the use case to map the AWS Lambda event to InputDTO.

        Args:
            input_dto (DynamoDBStreamsInputDTO): The input DTO containing event records.
        
        Returns:
            OutputDTO: The output DTO containing the list of table records.
        """

        # Build the output data for each record in the event stream
        streams_output_data: list[DynamoDBStreamsOutputData] = []

        for record in input_dto.records:
            try:
                table_record = DynamoDBStreamsOutputData(
                    table_name=self.__get_table_name_from_source_arn(record.event_source_arn),
                    event_id=record.event_id,
                    event_name=record.event_name,
                    event_version=record.event_version,
                    event_source=record.event_source,
                    event_source_service=self.__get_event_source_service(record.event_source),
                    aws_region=record.aws_region,
                    table_keys=record.record_data.keys,
                    table_new_image=record.record_data.new_image,
                    table_old_image=record.record_data.old_image,
                    sequence_number=record.record_data.sequence_number,
                    size_bytes=record.record_data.size_bytes,
                    stream_view_type=record.record_data.stream_view_type,
                    event_source_arn=record.event_source_arn,
                    event_timestamp=self.__get_event_timestamp(record.record_data.approx_ts),
                    event_date=self.__get_event_date(record.record_data.approx_ts)
                )

                streams_output_data.append(table_record)
            
            except Exception:
                table_name = self.__get_table_name_from_source_arn(record.event_source_arn)
                logger.exception(f"Error processing record with event ID {record.event_id} of source "
                                 f"table {table_name}")
                raise

        try:
            logger.info("Storing and syncing CDC data from DynamoDB Streams to a CDC table in the data catalog.")
            self.cdc_data_catalog_sync_adapter.store_and_sync_cdc_data(data=streams_output_data)

            logger.info("Storing and syncing SoR data from DynamoDB Streams to a SoR table in the data catalog.")
            self.cdc_data_catalog_sync_adapter.store_and_sync_sor_data(data=streams_output_data)

        except Exception:
            logger.exception("Error storing and syncing CDC and SoR data to the data catalog.")
            logger.exception(f"Event: {input_dto}")
            raise

        logger.info(f"Successfully stored {len(streams_output_data)} records from DynamoDB Streams.")

        return OutputDTO.ok(
            data={
                "total_table_records": len(streams_output_data),
                "cdc_table_name": f"cdc_{streams_output_data[0].table_name}",
                "sor_table_name": f"sor_{streams_output_data[0].table_name}"
            }
        )
