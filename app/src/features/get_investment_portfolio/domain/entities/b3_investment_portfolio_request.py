from dataclasses import dataclass, field
from datetime import datetime, UTC

from app.src.features.get_investment_portfolio.domain.entities.b3_stock import B3Stock
from app.src.features.cross.value_objects import DateFormat


@dataclass
class B3InvestmentPortfolioRequest:
    """
    Represents a B3 personal stock portfolio entity.

    Attributes:
        request_id (str): Unique identifier for the request
        source_url (str): The URL from which the portfolio data is sourced
        stocks_list (list[B3Stock]): List of stocks in the portfolio
        date_processed (str): The date when the portfolio was processed
    """

    request_id: str
    source_url: str
    stocks_list: list[B3Stock]
    date_processed: str = field(
        default_factory=lambda: datetime.now(UTC).strftime(DateFormat.DATE.value)
    )
