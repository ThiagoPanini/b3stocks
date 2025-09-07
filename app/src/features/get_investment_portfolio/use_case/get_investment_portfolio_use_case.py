from dataclasses import dataclass
from typing import Any

from app.src.features.cross.utils.log_utils import setup_logger
from app.src.features.get_investment_portfolio.domain.interfaces.investment_portfolio_request_adapter_interface import (
    IInvestmentPortfolioRequestAdapter
)
from app.src.features.cross.domain.dtos.output_dto import OutputDTO


logger = setup_logger(name=__name__)


@dataclass(frozen=True)
class GetInvestmentPortfolioUseCase:
    """
    Use case for fetching investment portfolio data.

    Attributes:
        investment_portfolio_request_adapter (IInvestmentPortfolioRequestAdapter):
            Adapter for fetching investment portfolio data.
    """

    investment_portfolio_request_adapter: IInvestmentPortfolioRequestAdapter

    def execute(self) -> Any:
        """
        Executes the use case to fetch investment portfolio data.

        Returns:
            B3InvestmentPortfolioRequest: An instance of B3InvestmentPortfolioRequest containing the portfolio data.
        """

        try:
            logger.info("Fetching investment portfolio data")
            portfolio = self.investment_portfolio_request_adapter.fetch_portfolio()
            logger.info("Successfully fetched investment portfolio data.")
        
        except Exception as e:
            logger.error(f"Error fetching investment portfolio data: {e}")
            raise e

        return OutputDTO.ok(
            data={
                "investment_portfolio": portfolio
            }
        )
