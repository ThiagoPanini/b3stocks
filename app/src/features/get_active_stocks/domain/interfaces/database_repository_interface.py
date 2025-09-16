from abc import ABC, abstractmethod
from app.src.features.get_active_stocks.domain.entities.stock import Stock


class IDatabaseRepository(ABC):
    """
    Interface for saving stocks basic data into a database repository.
    """

    @abstractmethod
    def batch_insert_items(self, items: list[Stock]) -> None:
        """
        Inserts a batch of stocks to the repository.

        Args:
            items (list[Stock]): The list of stocks to insert.
        """
