from dataclasses import dataclass
from typing import Any

from app.src.features.cross.domain.entities.batch_process import BatchProcess


@dataclass
class InputDTO:
    """
    Data Transfer Object for input data.

    Args:
        template_endpoint (str): The endpoint to fetch the email template.
        additional_data (Any): Any additional data required for processing.
    """
    template_endpoint: str
    batch_process: BatchProcess
