from abc import ABC, abstractmethod

from app.src.features.get_investment_portfolios.domain.entities.investment_portfolio import (
    InvestmentPortfolio
)


class IDatabaseRepository(ABC):
    """
    Interface for saving investment portfolio data into a database repository.
    """

    @abstractmethod
    def save_items(self, items: list[InvestmentPortfolio]) -> None:
        """
        Saves a list of investment portfolio data to the database repository.

        Args:
            items (list[InvestmentPortfolio]): The investment portfolio data to save.
        """
