from abc import ABC, abstractmethod

from app.src.features.cross.domain.entities.http_client_request_config import HTTPClientRequestConfig
from app.src.features.get_fundamentus_eod_stock_metrics.domain.entities.fundamentus_stock_metrics import (
    FundamentusStockMetrics
)


class IHTMLParserAdapter(ABC):
    """
    Interface for parsing raw text given by a HTTP request into stocks basic information.
    """

    @abstractmethod
    def parse_html_content(
        self,
        html_content: bytes,
        encoding: str,
        request_config: HTTPClientRequestConfig
    ) -> FundamentusStockMetrics:
        """
        Parses stocks metrics data from the raw HTML content of a HTTP response.

        Args:
            html_content (bytes): The raw HTML content of the HTTP response.
            encoding (str): The encoding used to decode the HTML content.
            request_config (HTTPClientRequestConfig): The object containing metadata of the request.

        Returns:
            A FundamentusStockMetrics entity containing the parsed stock metrics data.
        """
