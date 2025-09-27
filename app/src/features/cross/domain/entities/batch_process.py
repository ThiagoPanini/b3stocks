from dataclasses import dataclass, field
from datetime import datetime

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
    execution_date: str = field(
        default_factory=lambda: DateAndTimeUtils.datetime_now_str(
            timezone=Timezone.SAO_PAULO,
            format=DateFormat.DATE
        )
    )
    created_at: str = field(
        default_factory=lambda: DateAndTimeUtils.datetime_now_str(
            timezone=Timezone.SAO_PAULO,
            format=DateFormat.DATE_AND_TIME
        )
    )
    updated_at: str = field(
        default_factory=lambda: DateAndTimeUtils.datetime_now_str(
            timezone=Timezone.SAO_PAULO,
            format=DateFormat.DATE_AND_TIME
        )
    )
    finished_at: datetime = None
