from abc import ABC, abstractmethod

from app.src.features.get_investment_portfolio.domain.entities.investment_portfolio import (
    InvestmentPortfolio
)


class IDatabaseRepository(ABC):
    """
    Interface for saving investment portfolio data into a database repository.
    """

    @abstractmethod
    def save_item(self, item: InvestmentPortfolio) -> None:
        """
        Saves an investment portfolio data to the database repository.

        Args:
            item (InvestmentPortfolio): The investment portfolio data to save.
        """
