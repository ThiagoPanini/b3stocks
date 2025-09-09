from abc import ABC, abstractmethod

from app.src.features.get_investment_portfolio.domain.entities import InvestmentPortfolio


class IInvestmentPortfolioAdapter(ABC):
    """
    Interface for getting and parsing investment portfolio data.
    """

    @abstractmethod
    def fetch_portfolio(self) -> InvestmentPortfolio:
        """
        Fetches the investment portfolio data from a data source.

        Returns:
            InvestmentPortfolio: An instance of InvestmentPortfolio containing the portfolio data.
        """