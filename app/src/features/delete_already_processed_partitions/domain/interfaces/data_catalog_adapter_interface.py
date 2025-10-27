from abc import ABC, abstractmethod
from typing import Any

from app.src.features.delete_already_processed_partitions.domain.entities.table import Table


class IDataCatalogAdapter(ABC):
    """
    Interface for interacting with the data catalog.
    """
    
    @abstractmethod
    def get_partitions(self, database_name: str, table_name: str) -> dict[str, Any]:
        """
        Retrieves the list of partitions for a given table in the data catalog.

        Args:
            database_name (str): The name of the database.
            table_name (str): The name of the table.

        Returns:
            dict[str, Any]: A dictionary containing partition information for the specified table.
        """

    @abstractmethod
    def check_partition_exists(
        self,
        existing_partitions_values: list,
        partition_value_to_delete: str
    ) -> bool:
        """
        Checks if a specific partition exists in the given table.

        Args:
            existing_partitions_values (list): List of existing partition values.
            partition_value_to_delete (str): The value of the partition to check.

        Returns:
            bool: True if the partition exists, False otherwise.
        """
    
    @abstractmethod
    def delete_logical_partition_from_data_catalog(
        self,
        database_name: str,
        table_name: str,
        partition_values: list[str]
    ):
        """
        Deletes specified partitions from the given list of tables.

        Args:
            database_name (str): The name of the database.
            table_name (str): The name of the table.
            partition_values (list[str]): List of partition values to delete.
        """
    
    @abstractmethod
    def delete_physical_partition_from_storage(self, partition_path: str):
        """
        Deletes physical data associated with specified partitions from storage.

        Args:
            partition_path (str): The S3 path of the partition to delete.
        """

    @abstractmethod
    def delete_processed_partitions(self, tables: list[Table]) -> None:
        """
        Deletes both logical and physical partitions for the given tables.

        Args:
            tables (list[Table]): A list of Table objects containing partition information to delete.
        """
