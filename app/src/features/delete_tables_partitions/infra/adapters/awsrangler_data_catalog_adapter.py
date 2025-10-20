from typing import Any

import awswrangler as wr

from app.src.features.delete_tables_partitions.domain.interfaces.data_catalog_adapter_interface import (
    IDataCatalogAdapter
)
from app.src.features.delete_tables_partitions.domain.entities.table import Table
from app.src.features.cross.utils.log import LogUtils


logger = LogUtils.setup_logger(name=__name__)


class AWSRanglerDataCatalogAdapter(IDataCatalogAdapter):
    """
    Adapter for interacting with AWS Glue Data Catalog using AWS Wrangler.
    """

    def get_partitions(self, database_name: str, table_name: str) -> dict[str, Any]:
        """
        Retrieves the list of partitions for a given table in the data catalog.

        Args:
            database_name (str): The name of the database.
            table_name (str): The name of the table.

        Returns:
            dict[str, Any]: A dictionary containing partition information for the specified table.
        """
        try:
            table_partitions: dict[str, Any] =  wr.catalog.get_partitions(
                database=database_name,
                table=table_name
            )
            return table_partitions
        except Exception:
            logger.exception("Error retrieving partitions from data catalog")
            raise


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
        return True if partition_value_to_delete in existing_partitions_values else False


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
        try:
            wr.catalog.delete_partitions(
                database=database_name,
                table=table_name,
                partitions_values=partition_values
            )
        except Exception:
            logger.exception("Error deleting logical partition from data catalog")
            raise


    def delete_physical_partition_from_storage(self, partition_path: str):
        """
        Deletes physical data associated with specified partitions from storage.

        Args:
            partition_path (str): The S3 path of the partition to delete.
        """
        try:
            wr.s3.delete_objects([partition_path])
        except Exception:
            logger.exception("Error deleting physical partition from storage")
            raise


    def delete_partitions(self, tables: list[Table]) -> None:
        """
        Deletes both logical and physical partitions for the given tables.

        Args:
            tables (list[Table]): A list of Table objects containing partition information to delete.
        """

        for table in tables:
            table_partitions: dict[str, Any] = self.get_partitions(
                database_name=table.database_name,
                table_name=table.table_name
            )
            partitions_values = [p[0] for p in list(table_partitions.values())]
            partitions_paths = list(table_partitions.keys())

            for partition in table.partitions_config:
                if self.check_partition_exists(
                    existing_partitions_values=partitions_values,
                    partition_value_to_delete=partition.partition_value
                ):
                    # Delete logical partition from data catalog
                    self.delete_logical_partition_from_data_catalog(
                        database_name=table.database_name,
                        table_name=table.table_name,
                        partition_values=[
                            [partition.partition_value]
                        ]
                    )
                    # Delete physical partition from storage
                    partition_path_idx = partitions_values.index(partition.partition_value)
                    partition_path = partitions_paths[partition_path_idx]
                    self.delete_physical_partition_from_storage(
                        partition_path=partition_path
                    )
                    logger.info(
                        f"Successfully deleted partition {partition.partition_value} from table "
                        f"{table.database_name}.{table.table_name} on both data catalog and S3"
                    )
                else:
                    logger.info(
                        f"Partition {partition.partition_value} does not exist in table "
                        f"{table.database_name}.{table.table_name}"
                    )
