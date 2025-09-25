from typing import Any
from dataclasses import dataclass

from app.src.features.cross.utils.log import LogUtils
from app.src.features.cross.domain.dtos.output_dto import OutputDTO


logger = LogUtils.setup_logger(name=__name__)


@dataclass(frozen=True)
class CheckBatchProcessesCompletionUseCase:
    """
    Use case for checking the completion of batch processes related to stock metrics.
    """

    def execute(self, input_dto: Any) -> OutputDTO:
        """
        Implements the logic to execute the use case.

        Args:
            input_dto (StockMessagesInputDTO): The input DTO containing event records.

        Returns:
            OutputDTO: An instance of OutputDTO containing the result of the operation.
        """

        print(input_dto)
        return OutputDTO(success=True)
