from abc import ABC, abstractmethod

from app.src.features.cross.domain.entities.dynamodb_streams_output_data import DynamoDBStreamsOutputData


class ICDCDataCatalogSyncAdapter(ABC):
    """
    Interface for storing and synchronizing data from a change data capture (CDC) source with a
    data catalog.
    """

    @abstractmethod
    def store_and_sync_cdc_data(self, data: list[DynamoDBStreamsOutputData]) -> None:
        """
        Store data in a distributed storage repository and sync it with a data catalog.

        Args:
            data (list[DynamoDBStreamsOutputData]): List of data to be stored and synchronized.
        """
