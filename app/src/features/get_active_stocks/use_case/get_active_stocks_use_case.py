from dataclasses import dataclass

from app.src.features.cross.utils.log_utils import setup_logger
from app.src.features.cross.domain.interfaces.http_client_adapter import IHTTPClientAdapter
from app.src.features.get_active_stocks.domain.interfaces.html_parser_adapter_interface import (
    IHTMLParserAdapter
)
from app.src.features.get_active_stocks.domain.interfaces.database_repository_interface import (
    IDatabaseRepository
)
from app.src.features.get_active_stocks.domain.entities.stock import Stock
from app.src.features.cross.domain.entities.http_client_request_config import HTTPClientRequestConfig
from app.src.features.cross.domain.entities.http_client_retry_config import HTTPClientRetryConfig
from app.src.features.cross.domain.entities.http_client_response import HTTPClientResponse
from app.src.features.cross.domain.dtos.output_dto import OutputDTO


logger = setup_logger(__name__)


@dataclass(frozen=True)
class GetActiveStocksUseCase:
    """
    Use case for fetching active stocks data from a web source.

    Args:
        http_client_adapter (IHTTPClientAdapter): Adapter for making HTTP requests.
        html_parser_adapter (IHTMLParserAdapter): Adapter for parsing B3 stock tickers.
    """

    http_client_adapter: IHTTPClientAdapter
    html_parser_adapter: IHTMLParserAdapter
    database_repository: IDatabaseRepository


    def execute(self) -> OutputDTO:
        """
        Executes the use case to fetch active stocks data.

        Returns:
            OutputDTO: An instance of OutputDTO containing the result of the operation.
        """

        try:
            # Building a B3 stock tickers request entity
            request_config = HTTPClientRequestConfig(
                url="https://www.fundamentus.com.br/resultado.php",
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                                "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
                },
                timeout=10,
                retry_config=HTTPClientRetryConfig(
                    num_retries=3,
                    backoff_factor=0.1,
                    status_forcelist=[500, 502, 503, 504]
                )
            )

            logger.info(f"Scrapping active stocks raw content from URL {request_config.url}")
            http_response: HTTPClientResponse = self.http_client_adapter.get(request_config=request_config)

            logger.info("Parsing raw text from the HTTP response into stocks data")
            stocks: list[Stock] = self.html_parser_adapter.parse_html_content(
                html_content=http_response.content,
                encoding=http_response.encoding,
                request_config=request_config
            )

            logger.info(f"Saving {len(stocks)} active stocks data to the database repository")
            self.database_repository.batch_insert_items(items=stocks)

        except Exception:
            logger.exception(f"Error fetching and saving active stocks data")
            raise

        return OutputDTO.ok(
            data={
                "stocks": stocks[:2]
            }
        )