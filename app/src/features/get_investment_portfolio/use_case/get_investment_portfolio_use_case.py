import os
from dataclasses import dataclass
from typing import Any

from app.src.features.cross.utils.log_utils import setup_logger
from app.src.features.get_investment_portfolio.domain.interfaces.investment_portfolio_adapter_interface import (
    IInvestmentPortfolioAdapter
)
from app.src.features.get_investment_portfolio.domain.interfaces.database_repository_interface import (
    IDatabaseRepository
)
from app.src.features.cross.domain.dtos.output_dto import OutputDTO


logger = setup_logger(name=__name__)


@dataclass(frozen=True)
class GetInvestmentPortfolioUseCase:
    """
    Use case for fetching investment portfolio data.

    Attributes:
        investment_portfolio_request_adapter (IInvestmentPortfolioAdapter):
            Adapter for fetching investment portfolio data.
    """

    investment_portfolio_adapter: IInvestmentPortfolioAdapter
    database_repository: IDatabaseRepository

    def execute(self) -> Any:
        """
        Executes the use case to fetch investment portfolio data.

        Returns:
            B3InvestmentPortfolioRequest: An instance of B3InvestmentPortfolioRequest containing the portfolio data.
        """

        try:
            logger.info("Fetching investment portfolio data")
            investment_portfolio = self.investment_portfolio_adapter.fetch_portfolio()

            logger.info("Saving investment portfolio data to the database repository")
            self.database_repository.put_item(investment_portfolio)

        except Exception as e:
            logger.error(f"Error fetching investment portfolio data: {e}")
            raise e

        return OutputDTO.ok(
            data={
                "portfolio_source_url": investment_portfolio.source_url,
                "portfolio_owner_mail": investment_portfolio.owner_mail,
                "portfolio_table_name": os.getenv("DYNAMODB_INVESTMENT_PORTFOLIO_TABLE_NAME")
            }
        )
