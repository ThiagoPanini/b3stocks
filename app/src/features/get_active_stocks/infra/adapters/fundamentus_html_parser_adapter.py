from bs4 import BeautifulSoup

from app.src.features.cross.domain.entities.http_client_request_config import HTTPClientRequestConfig
from app.src.features.get_active_stocks.domain.interfaces.html_parser_adapter_interface import (
    IHTMLParserAdapter
)
from app.src.features.get_active_stocks.domain.entities.stock import Stock
from app.src.features.cross.utils.decorators import timing_decorator
from app.src.features.cross.utils.log_utils import setup_logger


class FundamentusHTMLParserAdapter(IHTMLParserAdapter):
    """
    Implementation of IHTMLParserAdapter that parses stock tickers from Fundamentus website.
    """

    def __init__(self):
        self.logger = setup_logger(__name__)


    @timing_decorator
    def parse_html_content(
        self,
        html_content: bytes,
        encoding: str,
        request_config: HTTPClientRequestConfig
    ) -> list[Stock]:
        """
        Parses stocks basic data from the raw HTML content of a HTTP response.

        Args:
            html_content (bytes): The raw HTML content of the HTTP response.
            encoding (str): The encoding used to decode the HTML content.
            request_config (HTTPClientRequestConfig): The object containing metadata of the request.

        Returns:
            A list of B3 stocks data extracted and parsed from the request.
        """

        # Decoding the raw HTML text and parsing it using BeautifulSoup
        try:
            html_text = html_content.decode(encoding)
            html_parsed = BeautifulSoup(html_text, "html.parser")
        except Exception as e:
            self.logger.exception(f"Error decoding and parsing HTML content: {e}")
            raise

        try:
            # Returning the HTML table containing cells that have stock information
            stock_tickers_cells = list({
                row.find("td")  # type: ignore
                for row in html_parsed.find_all("tr") if row.find("td") is not None  # type: ignore
            })

            # Extracting and consolidating information into a sorted list of dictionaries
            stock_tickers_info = sorted(
                [
                    {
                        "code": cell.find("a").text.upper().strip(),  # type: ignore
                        "company_name": cell.find("span").get("title").upper().strip()  # type: ignore
                    }
                    for cell in stock_tickers_cells
                ],
                key=lambda x: x["code"]
            )
        except Exception as e:
            self.logger.exception(f"Error extracting stock tickers from HTML content: {e}")
            raise

        try:
            # Adapting the result as instances of the expected entity
            stocks = [
                Stock(
                    code=info["code"],
                    company_name=info["company_name"],
                    request_config=request_config
                )
                for info in stock_tickers_info
            ]
        except Exception as e:
            self.logger.exception(f"Error adapting stock tickers to Stock entities: {e}")
            raise

        return stocks
