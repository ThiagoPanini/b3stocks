from dataclasses import dataclass, field
from datetime import datetime, UTC

from app.src.features.cross.domain.entities.http_client_request_config import HTTPClientRequestConfig
from app.src.features.cross.utils.date_and_time import DateAndTimeUtils
from app.src.features.cross.value_objects import Timezone


@dataclass()
class Stock:
    """
    Represents a B3 stock with basic information.
    """

    code: str
    company_name: str
    request_config: HTTPClientRequestConfig
    created_at: datetime = field(
        default_factory=lambda: DateAndTimeUtils.datetime_now(timezone=Timezone.SAO_PAULO)
    )
    updated_at: datetime = field(
        default_factory=lambda: DateAndTimeUtils.datetime_now(timezone=Timezone.SAO_PAULO)
    )

    def __post_init__(self):
        self.code = self.code.strip().upper()
        self.company_name = self.company_name.strip().upper()