from dataclasses import dataclass, field
from datetime import datetime, UTC

from app.src.features.cross.value_objects import InvestmentWebSite
from app.src.features.cross.domain.entities.http_client_request_config import HTTPClientRequestConfig


@dataclass
class B3StockTicker:
    """
    Represents a stock ticker entity with basic information.
    
    Attributes:
        code (str): The code that represents the stock ticker in B3 exchange.
        company_name (str): The name of the company associated with the stock ticker.
        date_extracted (str): The date when the stock ticker object was created.
    """

    code: str
    company_name: str
    web_site: InvestmentWebSite
    request_config: HTTPClientRequestConfig
    date_extracted: str = field(
        default_factory=lambda: datetime.now(UTC).strftime("%Y-%m-%d")
    )

    def __post_init__(self):
        """
        Post-initialization to ensure the code and the company_name are normalized.
        """
        self.code = self.code.strip().upper()
        self.company_name = self.company_name.strip().upper()
