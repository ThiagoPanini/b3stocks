from typing import Any
import json

from app.src.features.get_fundamentus_eod_stock_metrics.domain.dtos.stock_messages_input_dto import (
    StockMessagesInputDTO
)
from app.src.features.cross.domain.entities.stock_message_envelop import StockMessageEnvelop


class SQSMessagesLambdaEventMapper:
    """
    Maps a SQS Lambda event dict to a input Data Transfer Object (DTO) class
    """

    def map_event_to_input_dto(self, event: dict[str, Any]) -> StockMessagesInputDTO:
        """
        Maps a SQS Lambda event dict to a input Data Transfer Object (DTO) class

        Args:
            event (dict[str, Any]): The AWS Lambda event dict received from SQS.
        
        Returns:
            InputDTO: The mapped input Data Transfer Object.
        """
        messages = event.get("Records", [])
        if not messages:
            raise ValueError("No messages found in source event")

        # Map each SQS message to StockMessageEnvelop entity
        stock_messages: list[StockMessageEnvelop] = []
        for msg in messages:
            msg_body = json.loads(msg.get("body", "{}"))
            
            if "Message" not in msg_body:
                raise ValueError("Message key not found in SQS message body")
            else:
                try:
                    code = json.loads(msg_body["Message"])["code"]
                    total_expected_messages = json.loads(msg_body["Message"])["total_expected_messages"]
                except (json.JSONDecodeError, KeyError) as e:
                    raise ValueError("Invalid message format. The 'code' or 'total_expected_messages' "
                                     "keys is missing or malformed.")

                stock_message_envelop = StockMessageEnvelop(
                    code=code,
                    total_expected_messages=total_expected_messages
                )

                stock_messages.append(stock_message_envelop)

        return StockMessagesInputDTO(messages=stock_messages)
