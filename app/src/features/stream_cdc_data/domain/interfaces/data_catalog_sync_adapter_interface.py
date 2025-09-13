from abc import ABC, abstractmethod

import pandas as pd

from app.src.features.stream_cdc_data.domain.entities.table_record import TableRecord


class IDataCatalogSyncAdapter(ABC):
    """
    Interface for storing and synchronizing data with the data catalog.
    """

    @abstractmethod
    def store_and_sync_data(self, data: list[TableRecord]) -> None:
        """
        Store data in a distributed storage repository and sync with the data catalog.

        Args:
            data (list[TableRecord]): List of data to be stored.
        """
