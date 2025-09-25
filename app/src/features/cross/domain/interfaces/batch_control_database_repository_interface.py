from abc import ABC, abstractmethod

from app.src.features.cross.domain.entities.batch_process import BatchProcess


class IBatchControlDatabaseRepository(ABC):
    """
    Interface for saving batch process control data into a database repository.
    """

    @abstractmethod
    def update_batch_process_control(self, batch_process: BatchProcess) -> None:
        """
        Updates the batch process control record in the repository.

        Args:
            batch_process (BatchProcess): The batch process details to update.
        """
    

    @abstractmethod
    def check_batch_process_completion(self, batch_process: BatchProcess) -> None:
        """
        Checks if a batch process has completed based on the total and processed items.

        Args:
            batch_process (BatchProcess): The batch process details to check.
        """
