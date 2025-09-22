import os
from dataclasses import dataclass

from app.src.features.get_fundamentus_eod_stock_metrics.domain.dtos.stock_messages_input_dto import (
    StockMessagesInputDTO
)
from app.src.features.get_fundamentus_eod_stock_metrics.domain.interfaces.html_parser_adapter_interface import (
    IHTMLParserAdapter
)
from app.src.features.get_fundamentus_eod_stock_metrics.domain.interfaces.database_repository_interface import (
    IDatabaseRepository
)
from app.src.features.get_fundamentus_eod_stock_metrics.domain.entities.fundamentus_stock_metrics import (
    FundamentusStockMetrics
)

from app.src.features.cross.domain.interfaces.http_client_adapter import IHTTPClientAdapter
from app.src.features.cross.domain.entities.http_client_request_config import HTTPClientRequestConfig
from app.src.features.cross.domain.entities.http_client_retry_config import HTTPClientRetryConfig
from app.src.features.cross.domain.entities.http_client_response import HTTPClientResponse
from app.src.features.cross.domain.dtos.output_dto import OutputDTO
from app.src.features.cross.utils.log import LogUtils


logger = LogUtils.setup_logger(name=__name__)


@dataclass(frozen=True)
class GetFundamentusEodStockMetricsUseCase:
    """
    Use case for retrieving end-of-day stock metrics from Fundamentus web site.
    """

    http_client_adapter: IHTTPClientAdapter
    html_parser_adapter: IHTMLParserAdapter
    database_repository: IDatabaseRepository


    def execute(self, input_dto: StockMessagesInputDTO) -> OutputDTO:
        """
        Implements the logic to execute the use case.

        Args:
            input_dto (StockMessagesInputDTO): The input DTO containing event records.

        Returns:
            OutputDTO: An instance of OutputDTO containing the result of the operation.
        """
        
        stock_metrics_list: list[FundamentusStockMetrics] = []
        
        try:
            stock_codes = [message.code for message in input_dto.messages]
            logger.info(f"Getting and parsing metrics for the following {len(stock_codes)} "
                        f"stock codes: {', '.join(stock_codes)}")
            for stock_code in stock_codes:
                # Building a request config object to handle HTTP requests
                request_config = HTTPClientRequestConfig(
                    url=f"https://www.fundamentus.com.br/detalhes.php?papel={stock_code}",
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

                # Getting the raw HTML content from Fundamentus
                http_response: HTTPClientResponse = self.http_client_adapter.get(
                    request_config=request_config
                )

                # Parsing the HTML content to extract stock metrics
                stock_metrics: FundamentusStockMetrics = self.html_parser_adapter.parse_html_content(
                    html_content=http_response.content,
                    encoding=http_response.encoding,
                    request_config=request_config
                )

                stock_metrics_list.append(stock_metrics)
    
        except Exception:
            logger.exception(f"Error collecting and parsing stock metrics")
            raise

        try:
            logger.info(f"Saving {len(stock_metrics_list)} stock metrics to the database table")
            self.database_repository.batch_save_stock_metrics(stock_metrics_list)

        except Exception:
            logger.exception(f"Error saving stock metrics to the database repository")
            raise

        return OutputDTO.ok(
            data={
                "processed_stock_metrics": len(stock_metrics_list),
                "stock_codes": [stock_metrics.nome_papel for stock_metrics in stock_metrics_list],
                "dynamodb_table_name": os.getenv("DYNAMODB_FUNDAMENTUS_EOD_STOCK_METRICS_TABLE_NAME")
            }
        )
