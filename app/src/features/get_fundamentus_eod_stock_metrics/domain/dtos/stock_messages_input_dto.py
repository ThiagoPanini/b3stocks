from dataclasses import dataclass

from app.src.features.cross.domain.entities.stock_message import StockMessage


@dataclass
class StockMessagesInputDTO:
    """
    Data Transfer Object for input data on getting Fundamentus EOD stock metrics.
    """
    messages: list[StockMessage]
