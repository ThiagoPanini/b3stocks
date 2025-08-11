from dataclasses import dataclass


@dataclass
class B3StockTickerMessage:
    """
    Represents the body of a B3 stock ticker message.
    This class is used to serialize B3 stock ticker data for publishing to a topic.
    
    Attributes:
        code (str): The stock ticker code.
        company_name (str): The name of the company associated with the stock ticker.
        date_extracted (str): The date when the stock ticker was extracted.
    """

    code: str
    company_name: str
    date_extracted: str
