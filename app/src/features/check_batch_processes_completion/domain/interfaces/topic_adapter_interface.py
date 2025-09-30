from abc import ABC, abstractmethod

from app.src.features.cross.domain.entities.batch_process import BatchProcess


class ITopicAdapter(ABC):
    """
    Interface for publishing messages to a topic service (e.g., SNS).
    """
    
    @abstractmethod
    def publish_message(self, message: BatchProcess) -> None:
        """
        Publishes a message to the topic service.

        Args:
            message (BatchProcess): The message to publish.
        """
