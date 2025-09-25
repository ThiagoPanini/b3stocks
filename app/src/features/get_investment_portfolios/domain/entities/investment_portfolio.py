from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Optional
import re

from app.src.features.get_investment_portfolios.domain.entities import StockVariationControl
from app.src.features.cross.utils.date_and_time import DateAndTimeUtils
from app.src.features.cross.value_objects import Timezone


@dataclass
class InvestmentPortfolio:
    """
    Represents an investment portfolio entity.

    Attributes:
        owner_name (str): Portfolio owner's name
        owner_mail (str): Portfolio owner's email
        stocks (list[StockVariationControl]): List of stocks in the portfolio
        source_url (Optional[str]): URL of the portfolio source, if available
        created_at (datetime): Portfolio creation timestamp
        updated_at (datetime): Portfolio last update timestamp
    """

    owner_name: str
    owner_mail: str
    stocks: list[StockVariationControl]
    source_url: Optional[str] = None
    created_at: datetime = field(
        default_factory=lambda: DateAndTimeUtils.datetime_now(timezone=Timezone.SAO_PAULO)
    )
    updated_at: datetime = field(
        default_factory=lambda: DateAndTimeUtils.datetime_now(timezone=Timezone.SAO_PAULO)
    )

    def __post_init__(self):
        # Basic normalization
        self.owner_name = self.owner_name.strip()
        self.owner_mail = self.owner_mail.strip()

        # Simple email regex (not fully RFC compliant but good for validation)
        email_pattern = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
        if not email_pattern.match(self.owner_mail):
            raise ValueError(f"Invalid owner_mail format: {self.owner_mail}")