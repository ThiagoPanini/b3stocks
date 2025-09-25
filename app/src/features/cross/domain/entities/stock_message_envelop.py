from dataclasses import dataclass


@dataclass
class StockMessageEnvelop:
    """
    Represents the content of a message related to stock information.
    
    Attributes:
        code (str): The stock ticker code.
        total_expected_messages (int): The total number of expected messages related to the stock.
    """
    code: str
    total_expected_messages: int


    def __post_init__(self):
        self.code = self.code.upper().strip()
