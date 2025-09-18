from dataclasses import dataclass, field
from datetime import datetime, UTC

from app.src.features.cross.domain.entities.http_client_request_config import HTTPClientRequestConfig


@dataclass
class Stock:
    """
    Represents a B3 stock with basic information.
    """

    code: str
    company_name: str
    request_config: HTTPClientRequestConfig
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def __post_init__(self):
        self.code = self.code.strip().upper()
        self.company_name = self.company_name.strip().upper()