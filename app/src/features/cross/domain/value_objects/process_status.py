from enum import Enum


class ProcessStatus(Enum):
    """
    Enum representing the status of a process or task.
    """
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
