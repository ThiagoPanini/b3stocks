from abc import ABC, abstractmethod

from app.src.features.cross.domain.entities.http_client_request_config import HTTPClientRequestConfig
from app.src.features.cross.domain.entities.http_client_response import HTTPClientResponse
from app.src.features.get_b3_stock_tickers.domain.entities.b3_stock_ticker import B3StockTicker


class IHTMLParserAdapter(ABC):
    """
    Interface for parsing B3 stock tickers from a raw text given by a HTTP request.
    """

    @abstractmethod
    def parse_html_content(
        self,
        html_content: bytes,
        encoding: str,
        request_config: HTTPClientRequestConfig
    ) -> list[B3StockTicker]:
        """
        Parses stock tickers from the raw HTML content of a HTTP response.

        Args:
            html_content (bytes): The raw HTML content of the HTTP response.
            encoding (str): The encoding used to decode the HTML content.
            request_config (HTTPClientRequestConfig): The object containing metadata of the request.

        Returns:
            A list of B3 stock tickers extracted and parsed from the request.
        """
