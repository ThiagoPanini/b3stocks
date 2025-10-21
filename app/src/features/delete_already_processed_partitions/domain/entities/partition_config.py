from dataclasses import dataclass


@dataclass
class PartitionConfig:
    """
    Represents the partition configuration for a database table.

    Attributes:
        partition_column (str): The column used for partitioning.
        partition_value (str): The value of the partition.
    """
    partition_column: str
    partition_value: str
