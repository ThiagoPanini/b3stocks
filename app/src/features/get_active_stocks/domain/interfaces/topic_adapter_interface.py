from abc import ABC, abstractmethod
from typing import Any

from app.src.features.cross.domain.entities.stock_message_envelop import StockMessageEnvelop


class ITopicAdapter(ABC):
    """
    Interface for publishing messages to a topic service (e.g., SNS).
    """
    
    @abstractmethod
    def batch_publish_messages(self, messages: list[StockMessageEnvelop]) -> None:
        """
        Publishes a batch of messages to a topic service.

        Args:
            messages (list[StockMessageEnvelop]): A list of messages to publish.
        """
