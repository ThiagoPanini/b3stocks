from abc import ABC, abstractmethod


class IStorageRepository(ABC):
    """
    Interface for storage repository.
    """

    @abstractmethod
    def store_data(self, data: list[dict]) -> None:
        """
        Store data in the storage.

        Args:
            data (list[dict]): List of data to be stored.
        """
        pass