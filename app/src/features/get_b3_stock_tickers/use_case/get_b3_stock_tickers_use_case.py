import os
from uuid import uuid4
from dataclasses import dataclass

from app.src.features.cross.utils.log_utils import setup_logger
from app.src.features.cross.domain.interfaces.http_client_adapter import IHTTPClientAdapter
from app.src.features.cross.domain.entities.http_client_request_config import HTTPClientRequestConfig
from app.src.features.cross.domain.entities.http_client_retry_config import HTTPClientRetryConfig
from app.src.features.cross.domain.entities.http_client_response import HTTPClientResponse
from app.src.features.get_b3_stock_tickers.domain.interfaces.html_parser_adapter_interface import (
    IHTMLParserAdapter
)
from app.src.features.get_b3_stock_tickers.domain.interfaces.topic_adapter_interface import (
    ITopicAdapter
)
from app.src.features.get_b3_stock_tickers.domain.entities.b3_stock_ticker_message import (
    B3StockTickerMessage
)
from app.src.features.get_b3_stock_tickers.domain.dtos.output_dto import OutputDTO


logger = setup_logger(__name__)


@dataclass(frozen=True)
class GetB3StockTickersUseCase:
    """
    Use case for fetching B3 stock tickers.
    
    Attributes:
        http_client_adapter (IHTTPClientAdapter): Adapter for making HTTP requests.
        html_parser_adapter (IHTMLParserAdapter): Adapter for parsing B3 stock tickers.
        database_repository (IDatabaseRepository): Repository for storing B3 stock tickers.
        queue_adapter (IQueueAdapter): Adapter for sending messages to a queue.
    """

    http_client_adapter: IHTTPClientAdapter
    html_parser_adapter: IHTMLParserAdapter
    topic_adapter: ITopicAdapter


    def execute(self) -> list[str]:
        """
        Executes the use case to fetch B3 stock tickers.
        
        Returns:
            A list of stock ticker codes from B3.
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

            logger.info(f"Fetching B3 stock tickers from {request_config.url}")
            http_response: HTTPClientResponse = self.http_client_adapter.get(request_config=request_config)

            logger.info("Parsing B3 stock tickers from the HTTP response with BeautifulSoup")
            b3_stock_tickers_list = self.html_parser_adapter.parse_html_content(
                html_content=http_response.content,
                encoding=http_response.encoding,
                request_config=request_config
            )

            # Build messages object and publish it to a topic
            messages = [
                B3StockTickerMessage(
                    code=b3_stock_ticker.code,
                    company_name=b3_stock_ticker.company_name,
                    date_extracted=b3_stock_ticker.date_extracted
                )
                for b3_stock_ticker in b3_stock_tickers_list
            ]
            logger.info(f"Publishing {len(messages)} B3 stock tickers messages to the topic")
            self.topic_adapter.batch_publish_messages(messages=messages)

            return OutputDTO.ok(
                data={
                    "total_tickers": len(b3_stock_tickers_list),
                    "sns_topic_name": os.getenv("SNS_B3_STOCK_TICKERS_TOPIC_NAME")
                }
            )
        
        except Exception as e:
            logger.exception(f"An error occurred while executing the use case: {e}")
            return OutputDTO.fail(error=str(e))
