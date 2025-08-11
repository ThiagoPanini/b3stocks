from dataclasses import dataclass, field
from typing import Any, Optional

from app.src.features.cross.domain.entities.http_client_retry_config import HTTPClientRetryConfig


@dataclass(frozen=True)
class HTTPClientRequestConfig:
    """
    Represents the configuration for an HTTP client request.

    Attributes:
        url (str): The URL to which the request is made.
        headers (Optional[dict[str, Any]]): Optional headers to include in the request.
        timeout (int): The timeout for the request in seconds.
        retry_config (Optional[HTTPClientRetryConfig]): Optional retry configuration for the request.
        request_kwargs (Optional[dict[str, Any]]): Additional keyword arguments for the request.
    """

    url: str
    headers: Optional[dict[str, Any]] = field(default_factory=dict)
    timeout: int = 10
    retry_config: Optional[HTTPClientRetryConfig] = None
    request_kwargs: Optional[dict[str, Any]] = field(default_factory=dict)

    def to_dict(self) -> dict:
        """
        Converts the request configuration to a dictionary.

        Returns:
            A dictionary representation of the request configuration.
        """
        return {
            "url": self.url,
            "headers": self.headers,
            "timeout": self.timeout,
            "retry_config": self.retry_config.to_dict() if self.retry_config else None,
            "request_kwargs": self.request_kwargs
        }
