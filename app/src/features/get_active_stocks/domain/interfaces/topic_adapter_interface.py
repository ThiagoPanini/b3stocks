from abc import ABC, abstractmethod
from typing import Any

from app.src.features.get_active_stocks.domain.entities.stock_message import StockMessage


class ITopicAdapter(ABC):
    """
    Interface for publishing messages to a topic service (e.g., SNS).
    """
    
    @abstractmethod
    def batch_publish_messages(self, messages: list[StockMessage]) -> None:
        """
        Publishes a batch of messages to a topic service.

        Args:
            messages (list[StockMessage]): A list of messages to publish.
        """
