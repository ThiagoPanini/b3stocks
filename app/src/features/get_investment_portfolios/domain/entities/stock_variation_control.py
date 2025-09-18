from dataclasses import dataclass, field
from typing import Optional

from .variation_threshold import VariationThreshold
from app.src.features.cross.value_objects import StockType


@dataclass
class StockVariationControl:
    """
    Represents a stock entity with basic information.

    Attributes:
        company_name (str): The name of the company.
        ticker_code (str): The code that represents the stock in B3 exchange.
        stock_type (Optional[StockType]): The type of stock derived from the ticker code.
        notify_on_threshold (bool): Whether to notify when thresholds are crossed.
        variation_thresholds (VariationThreshold): The variation thresholds for notifications.
    """

    company_name: str
    ticker_code: str
    stock_type: Optional[StockType]
    notify_on_threshold: bool
    variation_thresholds: VariationThreshold

    def __post_init__(self):
        # Basic normalization
        self.company_name = self.company_name.strip().upper()
        self.ticker_code = self.ticker_code.strip().upper()
        
        # Initializing stock_type based on ticker code suffix
        suffix = ''.join(filter(str.isdigit, self.ticker_code))
        self.stock_type = StockType.from_ticker_suffix(suffix)