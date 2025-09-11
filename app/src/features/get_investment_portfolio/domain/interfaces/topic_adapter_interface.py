from abc import ABC, abstractmethod
from typing import Any

from app.src.features.get_investment_portfolio.domain.entities.b3_investment_portfolio_request import (
    B3InvestmentPortfolioRequest
)


class ITopicAdapter(ABC):
    """
    Interface for publishing messages to a topic (e.g., SNS).
    """

    @abstractmethod
    def publish_message(self, messages: B3InvestmentPortfolioRequest) -> None:
        """
        Publishes a list of messages to the topic.

        Args:
            messages (list[B3InvestmentPortfolioRequest]): The messages to publish (should be serializable).
        """

