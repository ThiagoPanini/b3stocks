from abc import ABC, abstractmethod

from app.src.features.get_investment_portfolio.domain.entities.b3_investment_portfolio_request import (
    B3InvestmentPortfolioRequest
)


class IInvestmentPortfolioRequestAdapter(ABC):
    """
    Interface for adapting investment portfolio requests.
    """

    @abstractmethod
    def fetch_portfolio(self) -> B3InvestmentPortfolioRequest:
        """
        Fetches the investment portfolio data.

        Returns:
            B3InvestmentPortfolioRequest: An instance of B3InvestmentPortfolioRequest containing the portfolio data.
        """