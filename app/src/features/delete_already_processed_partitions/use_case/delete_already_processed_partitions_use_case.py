from dataclasses import dataclass

import awswrangler as wr

from app.src.features.delete_already_processed_partitions.domain.entities.table import Table
from app.src.features.delete_already_processed_partitions.domain.interfaces.data_catalog_adapter_interface import (
    IDataCatalogAdapter
)

from app.src.features.cross.utils.log import LogUtils
from app.src.features.cross.domain.dtos.output_dto import OutputDTO


logger = LogUtils.setup_logger(name=__name__)


@dataclass
class DeleteAlreadyProcessedPartitionsUseCase:
    """
    Use case for checking and deleting partitions on SoR/bronze layer.
    """

    data_catalog_adapter: IDataCatalogAdapter


    def execute(self) -> OutputDTO:
        """
        Implements the logic to execute the use case.

        Returns:
            OutputDTO: An instance of OutputDTO containing the result of the operation.
        """
        try:
            tables_to_cleanup: list[Table] = [
                Table(
                    database_name="db_b3stocks_analytics_sor",
                    table_name="sor_tbl_b3stocks_active_stocks"
                ),
                Table(
                    database_name="db_b3stocks_analytics_sor",
                    table_name="sor_tbl_b3stocks_fundamentus_eod_stock_metrics"
                ),
                Table(
                    database_name="db_b3stocks_analytics_sor",
                    table_name="sor_tbl_b3stocks_batch_process_control"
                )
            ]

            logger.info(f"Deleting already processed partitions for pre-selected tables")
            self.data_catalog_adapter.delete_processed_partitions(tables=tables_to_cleanup)

            return OutputDTO.ok(
                data={
                    "tables_cleaned_up": tables_to_cleanup,
                }
            )
        
        except Exception:
            logger.exception("Error executing the use case")
            raise