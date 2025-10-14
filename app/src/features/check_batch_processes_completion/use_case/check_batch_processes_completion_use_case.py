import os
from dataclasses import dataclass

from app.src.features.check_batch_processes_completion.domain.interfaces.topic_adapter_interface import (
    ITopicAdapter
)

from app.src.features.cross.domain.dtos.dynamodb_streams_input_dto import DynamoDBStreamsInputDTO
from app.src.features.cross.utils.log import LogUtils
from app.src.features.cross.domain.dtos.output_dto import OutputDTO
from app.src.features.cross.domain.entities.batch_process import BatchProcess
from app.src.features.cross.domain.value_objects import (
    BatchProcessName,
    ProcessStatus
)


logger = LogUtils.setup_logger(name=__name__)


@dataclass(frozen=True)
class CheckBatchProcessesCompletionUseCase:
    """
    Use case for checking the completion of batch processes related to stock metrics.
    """

    topic_adapter: ITopicAdapter


    def execute(self, input_dto: DynamoDBStreamsInputDTO) -> OutputDTO:
        """
        Implements the logic to execute the use case.

        Args:
            input_dto (DynamoDBStreamsInputDTO): The input DTO containing event records.

        Returns:
            OutputDTO: An instance of OutputDTO containing the result of the operation.
        """

        try:
            logger.info("Checking if any records in the stream event indicate a batch process completion")
            for record in input_dto.records:
                table_new_image = record.record_data.new_image

                batch_process = BatchProcess(
                    process_name=BatchProcessName(table_new_image["process_name"]),
                    total_items=int(table_new_image["total_items"]),
                    processed_items=int(table_new_image["processed_items"]),
                    process_status=ProcessStatus(table_new_image["process_status"]),
                    execution_date=table_new_image["execution_date"],
                    created_at=table_new_image["created_at"],
                    updated_at=table_new_image["updated_at"],
                    finished_at=table_new_image.get("finished_at", None)
                )

                if batch_process.process_status == ProcessStatus.COMPLETED:
                    logger.info(
                        f"Batch process '{batch_process.process_name.value}' has been completed "
                        f"at {batch_process.finished_at}. Sending to SNS topic for further processing."
                    )
                    self.topic_adapter.publish_message(batch_process)
                else:
                    logger.info(
                        f"Batch process '{batch_process.process_name.value}' is not yet completed. "
                        f"Current status: {batch_process.process_status.value}."
                    )
        except Exception:
            logger.exception("Error checking batch processes completion")
            raise

        return OutputDTO.ok(
            data={
                "process_name": batch_process.process_name.value,
                "process_status": batch_process.process_status.value,
                "sns_topic_name": os.getenv("SNS_BATCH_PROCESSES_COMPLETION_TOPIC_NAME")
            }
        )
