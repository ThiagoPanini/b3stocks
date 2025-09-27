from dataclasses import dataclass, field
from datetime import date, datetime

from app.src.features.cross.utils.date_and_time import DateAndTimeUtils
from app.src.features.cross.value_objects import (
    BatchProcessName,
    ProcessStatus,
    Timezone,
    DateFormat
)


@dataclass
class BatchProcess:
    process_name: BatchProcessName
    total_items: int
    processed_items: int = 0
    process_status: ProcessStatus = ProcessStatus.IN_PROGRESS
    execution_date: date = field(
        default_factory=lambda: DateAndTimeUtils.now(
            output_type="date",
            timezone=Timezone.SAO_PAULO,
        )
    )
    created_at: datetime = field(
        default_factory=lambda: DateAndTimeUtils.now(
            output_type="datetime",
            timezone=Timezone.SAO_PAULO,
        )
    )
    updated_at: datetime = field(
        default_factory=lambda: DateAndTimeUtils.now(
            output_type="datetime",
            timezone=Timezone.SAO_PAULO,
        )
    )
    finished_at: datetime = None
