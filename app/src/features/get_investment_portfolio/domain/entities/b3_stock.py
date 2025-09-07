from dataclasses import dataclass, field
from typing import Optional

from app.src.features.cross.value_objects import StockType


@dataclass
class B3Stock:
    """
    Represents a stock entity with basic information.

    Attributes:
        stock_code (str): The code that represents the stock in B3 exchange.
    """

    stock_code: str
    product_name: Optional[str]
    company_cnpj: Optional[str]
    isin_code: Optional[str]
    stock_type: StockType = field(default=None)

    def __post_init__(self):
        """
        Post-initialization to normalize stock code and determine stock type.
        """
        self.stock_code = self.stock_code.strip().upper()

        stock_suffix = ''.join(filter(str.isdigit, self.stock_code))
        self.stock_type = StockType.from_ticker_suffix(stock_suffix)
