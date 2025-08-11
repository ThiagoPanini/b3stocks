import logging

import requests

from app.src.features.cross.utils.log_utils import setup_logger
from app.src.features.cross.domain.interfaces.http_client_adapter import IHTTPClientAdapter
from app.src.features.cross.domain.entities.http_client_request_config import HTTPClientRequestConfig
from app.src.features.cross.domain.entities.http_client_response import HTTPClientResponse


class RequestsHTTPClientAdapter(IHTTPClientAdapter):
    """
    Implementation of IHTTPClientAdapter that uses the requests library to make HTTP requests.
    """

    def __init__(self, logger: logging.Logger = setup_logger(__name__)):
        self.logger = logger


    def get(self, request_config: HTTPClientRequestConfig) -> HTTPClientResponse:
        """
        Performs a GET request to the specified URL with optional headers and parameters.

        Args:
            request_config (HTTPClientRequestConfig): Configuration for the HTTP request.

        Returns:
            An HTTPClientResponse object representing the response.
        """

        # Create a request session
        session = requests.Session()

        # Set retry configuration for the session
        retry_config = requests.adapters.Retry(
            total=request_config.retry_config.num_retries,
            backoff_factor=request_config.retry_config.backoff_factor,
            status_forcelist=request_config.retry_config.status_forcelist
        )

        http_adapter = requests.adapters.HTTPAdapter(max_retries=retry_config)
        session.mount("https://", http_adapter)
        session.mount("http://", http_adapter)

        try:
            r = session.get(
                url=request_config.url,
                headers=request_config.headers,
                timeout=request_config.timeout,
                **request_config.request_kwargs
            )

        except requests.Timeout as to_error:
            self.logger.exception(
                msg=f"Timeout error while accessing URL: {request_config.url}",
                exc_info=to_error
            )

        except requests.ConnectionError as conn_error:
            self.logger.exception(
                msg=f"Connection error while accessing URL: {request_config.url}",
                exc_info=conn_error
            )

        except requests.HTTPError as http_error:
            self.logger.exception(
                msg=f"HTTP error while accessing URL: {request_config.url}",
                exc_info=http_error
            )

        return HTTPClientResponse(
            url=r.url,
            status_code=r.status_code,
            content=r.content,
            encoding=r.encoding,
            elapsed_time=r.elapsed.total_seconds()
        )
