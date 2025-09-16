import os
from dataclasses import dataclass
from typing import Any

from app.src.features.cross.utils.log_utils import setup_logger
from app.src.features.get_investment_portfolios.domain.interfaces.investment_portfolio_adapter_interface import (
    IInvestmentPortfolioAdapter
)
from app.src.features.get_investment_portfolios.domain.interfaces.database_repository_interface import (
    IDatabaseRepository
)
from app.src.features.cross.domain.dtos.output_dto import OutputDTO


logger = setup_logger(name=__name__)


@dataclass(frozen=True)
class GetInvestmentPortfolioUseCase:
    """
    Use case for fetching investment portfolio data.

    Args:
        investment_portfolio_request_adapter (IInvestmentPortfolioAdapter):
            Adapter for fetching investment portfolio data.
    """

    investment_portfolio_adapter: IInvestmentPortfolioAdapter
    database_repository: IDatabaseRepository

    def execute(self) -> Any:
        """
        Executes the use case to fetch investment portfolio data.

        Returns:
            OutputDTO: An instance of OutputDTO containing the result of the operation.
        """

        try:
            logger.info("Fetching investment portfolios data")
            investment_portfolios = self.investment_portfolio_adapter.fetch_portfolio()

            logger.info("Saving investment portfolios to the database repository")
            self.database_repository.save_items(investment_portfolios)

        except Exception:
            logger.error(f"Error fetching investment portfolio data")
            raise

        return OutputDTO.ok(
            data={
                "portfolios_table_name": os.getenv("DYNAMODB_INVESTMENT_PORTFOLIO_TABLE_NAME")
            }
        )
