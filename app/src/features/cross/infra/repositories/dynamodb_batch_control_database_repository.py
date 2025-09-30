import os
from datetime import datetime

import boto3
from pynamodb.models import Model
from pynamodb.attributes import (
    UnicodeAttribute,
    NumberAttribute,
)
from pynamodb.exceptions import DoesNotExist

from app.src.features.cross.domain.interfaces.batch_control_database_repository_interface import (
    IBatchControlDatabaseRepository
)
from app.src.features.cross.domain.entities.batch_process import BatchProcess
from app.src.features.cross.utils.date_and_time import DateAndTimeUtils
from app.src.features.cross.utils.serialization import SerializationUtils
from app.src.features.cross.utils.log import LogUtils
from app.src.features.cross.value_objects import (
    Timezone,
    ProcessStatus
)


class BatchProcessControlModel(Model):
    """
    PynamoDB model for batch process control data.
    """
    class Meta:
        table_name = os.getenv("DYNAMODB_BATCH_PROCESS_CONTROL_TABLE_NAME")
        region = boto3.session.Session().region_name

    process_name = UnicodeAttribute(hash_key=True)
    total_items = NumberAttribute()
    processed_items = NumberAttribute()
    process_status = UnicodeAttribute()
    execution_date = UnicodeAttribute(range_key=True)
    created_at = UnicodeAttribute()
    updated_at = UnicodeAttribute()
    finished_at = UnicodeAttribute(null=True)

    def __init__(self, *args, **kwargs):
        self.Meta.table_name = os.getenv("DYNAMODB_BATCH_PROCESS_CONTROL_TABLE_NAME")
        super().__init__(*args, **kwargs)

    
class DynamoDBBatchControlDatabaseRepository(IBatchControlDatabaseRepository):
    """
    Implementation of the batch process control repository using DynamoDB.
    """

    def __init__(self):
        self.logger = LogUtils.setup_logger(name=__name__)

    
    def update_batch_process_control(self, batch_process: BatchProcess) -> None:
        """
        Updates the batch process control record in the repository.

        Args:
            batch_process (BatchProcess): The batch process details to update.
        """
        serialized_item = SerializationUtils.json_serialize(batch_process)
        try:
            current_batch_process = BatchProcessControlModel.get(
                serialized_item["process_name"],
                serialized_item["execution_date"]
            )

            # If there is a completed process with the same name and date, reset it
            if current_batch_process.process_status == ProcessStatus.COMPLETED.value:
                current_batch_process.update(
                    actions=[
                        BatchProcessControlModel.process_status.set(ProcessStatus.IN_PROGRESS.value),
                        BatchProcessControlModel.processed_items.set(int(serialized_item["processed_items"])),
                        BatchProcessControlModel.total_items.set(serialized_item["total_items"]),
                        BatchProcessControlModel.created_at.set(serialized_item["created_at"]),
                        BatchProcessControlModel.updated_at.set(serialized_item["updated_at"]),
                        BatchProcessControlModel.finished_at.set(None),
                    ]
                )
            else:
                # Updates the batch record with the new processed items count and updated timestamp
                current_batch_process.update(
                    actions=[
                        BatchProcessControlModel.process_status.set(ProcessStatus.IN_PROGRESS.value),
                        BatchProcessControlModel.processed_items.add(int(serialized_item["processed_items"])),
                        BatchProcessControlModel.updated_at.set(serialized_item["updated_at"]),
                    ]
                )

        except DoesNotExist:
            # If item does not exist, create a new one  
            try:
                item = BatchProcessControlModel(**serialized_item)
                item.save()
            except Exception:
                self.logger.exception("Failed to save new batch process control record to DynamoDB.")
                raise


    def check_batch_process_completion(self, batch_process: BatchProcess) -> None:
        """
        Checks if a batch process has completed based on the total and processed items.

        Args:
            batch_process (BatchProcess): The batch process details to check.
        """

        serialized_item = SerializationUtils.json_serialize(batch_process)
        current_batch_process = BatchProcessControlModel.get(
            serialized_item["process_name"],
            serialized_item["execution_date"]
        )

        if int(current_batch_process.processed_items) >= int(current_batch_process.total_items):
            # Marks the process as completed
            finished_at: datetime = DateAndTimeUtils.now(
                output_type="datetime",
                timezone=Timezone.SAO_PAULO
            )
            current_batch_process.update(
                actions=[
                    BatchProcessControlModel.process_status.set(ProcessStatus.COMPLETED.value),
                    BatchProcessControlModel.finished_at.set(finished_at.isoformat()),
                    BatchProcessControlModel.updated_at.set(serialized_item["updated_at"]),
                ]
            )
