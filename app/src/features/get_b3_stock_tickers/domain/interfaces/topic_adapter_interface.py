from abc import ABC, abstractmethod
from typing import Any

from app.src.features.get_b3_stock_tickers.domain.entities.b3_stock_ticker_message import (
    B3StockTickerMessage
)


class ITopicAdapter(ABC):
    """
    Interface for publishing messages to a topic (e.g., SNS).
    """

    @abstractmethod
    def publish_messages(self, messages: list[B3StockTickerMessage]) -> None:
        """
        Publishes a list of messages to the topic.

        Args:
            messages (list[B3StockTickerMessage]): The messages to publish (should be serializable).
        """

    
    @abstractmethod
    def batch_publish_messages(self, messages: list[B3StockTickerMessage]) -> None:
        """
        Publishes a batch of messages to the topic.

        Args:
            messages (list[B3StockTickerMessage]): A list of messages to publish (should be serializable).
        """
