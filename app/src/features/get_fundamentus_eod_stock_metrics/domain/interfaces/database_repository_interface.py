from abc import ABC, abstractmethod
from app.src.features.get_fundamentus_eod_stock_metrics.domain.entities.fundamentus_stock_metrics import (
    FundamentusStockMetrics
)


class IDatabaseRepository(ABC):
    """
    Interface for saving Fundamentus stock metrics data into a database repository.
    """

    @abstractmethod
    def batch_save_stock_metrics(self, stock_metrics_list: list[FundamentusStockMetrics]) -> None:
        """
        Saves a batch of stock metrics data to the repository.

        Args:
            stock_metrics_list (list[FundamentusStockMetrics]): List of stock metrics to save.
        """
        pass
