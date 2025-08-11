from abc import ABC, abstractmethod

from app.src.features.cross.domain.entities.http_client_request_config import HTTPClientRequestConfig
from app.src.features.cross.domain.entities.http_client_response import HTTPClientResponse


class IHTTPClientAdapter(ABC):
    """
    Interface for HTTP client adapters.
    """

    @abstractmethod
    def get(self, request_config: HTTPClientRequestConfig) -> HTTPClientResponse:
        """
        Performs a GET request to the specified URL with optional headers and parameters.

        Args:
            request_config (HTTPClientRequestConfig): Configuration for the HTTP request.

        Returns:
            An HTTPClientResponse object representing the response.
        """
