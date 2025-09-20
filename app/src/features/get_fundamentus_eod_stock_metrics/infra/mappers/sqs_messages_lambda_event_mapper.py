from typing import Any
import json

from app.src.features.get_fundamentus_eod_stock_metrics.domain.dtos.stock_messages_input_dto import (
    StockMessagesInputDTO
)
from app.src.features.cross.domain.entities.stock_message import StockMessage


class SQSMessagesLambdaEventMapper:
    """
    Maps an SQS Lambda event dict to a input Data Transfer Object (DTO) class
    """

    def map_event_to_input_dto(self, event: dict[str, Any]) -> StockMessagesInputDTO:
        """
        Maps a SQS Lambda event dict to a input Data Transfer Object (DTO) class

        Args:
            event (dict[str, Any]): The AWS Lambda event dict received from SQS.
        """
        messages = event.get("Records", [])
        if not messages:
            raise ValueError("No messages found in source event")

        # Map each SQS message to StockMessage entity
        stock_messages = [
            StockMessage(
                code=json.loads(json.loads(msg["body"])["Message"])["code"],
            )
            for msg in messages
        ]

        return StockMessagesInputDTO(messages=stock_messages)
