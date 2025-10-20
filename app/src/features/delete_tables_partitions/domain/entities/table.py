from dataclasses import dataclass, field

from app.src.features.delete_tables_partitions.domain.entities.partition_config import PartitionConfig
from app.src.features.cross.utils.date_and_time import DateAndTimeUtils
from app.src.features.cross.domain.value_objects import (
    Timezone,
    DateFormat
)


@dataclass
class Table:
    """
    Represents a database table with its associated partition configuration.

    Attributes:
        database_name (str): The name of the database.
        table_name (str): The name of the table.
        partition_config (PartitionConfig): The partition configuration for the table.
    """
    database_name: str
    table_name: str
    partitions_config: list[PartitionConfig] = field(
        default_factory=lambda: [
            PartitionConfig(
                partition_column="execution_date",
                partition_value=DateAndTimeUtils.now(
                    output_type="string",
                    timezone=Timezone.SAO_PAULO,
                    str_format=DateFormat.DATE
                )
            )
        ]
    )


    def __post_init__(self):
        self.database_name = self.database_name.strip().lower()
        self.table_name = self.table_name.strip().lower()
