from dataclasses import dataclass


@dataclass
class StockMessage:
    """
    Represents the body of a stock message.
    This class is used to serialize stock data for publishing to a topic.
    
    Attributes:
        code (str): The stock ticker code.
    """
    code: str


    def __post_init__(self):
        # Ensuring the stock code is always uppercase
        self.code = self.code.upper().strip()