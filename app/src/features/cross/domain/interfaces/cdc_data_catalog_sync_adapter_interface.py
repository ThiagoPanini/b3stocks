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
        Store CDC data in a distributed storage repository and sync it with a data catalog.

        Args:
            data (list[DynamoDBStreamsOutputData]): List of CDC data to be stored and synchronized.
        """
    
    @abstractmethod
    def store_and_sync_sor_data(self, data: list[DynamoDBStreamsOutputData]) -> None:
        """
        Store SoR (raw) data in a distributed storage repository and sync it with a data catalog.
        
        In fact, this method would be very similar to store_and_sync_cdc_data, but this considers
        only the extraction and storage of raw data (e.g. dynamodb new image) from the CDC source.

        Args:
            data (list[DynamoDBStreamsOutputData]): List of data to be stored and synchronized.
        """
