from abc import ABC, abstractmethod

from app.src.features.get_investment_portfolios.domain.entities import InvestmentPortfolio


class IInvestmentPortfolioAdapter(ABC):
    """
    Interface for getting and parsing investment portfolio data.
    """

    @abstractmethod
    def fetch_portfolio(self) -> list[InvestmentPortfolio]:
        """
        Fetches the investment portfolio data from a data source.

        Returns:
            list[InvestmentPortfolio]:
                A list of InvestmentPortfolio instances containing, each one, an individual
                portfolio data.
        """