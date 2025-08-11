from typing import Any

from app.src.features.cross.infra.adapters.requests_http_client_adapter import RequestsHTTPClientAdapter
from app.src.features.get_b3_stock_tickers.use_case.get_b3_stock_tickers_use_case import (
    GetB3StockTickersUseCase
)
from app.src.features.get_b3_stock_tickers.infra.adapters.fundamentus_html_parser_adapter import (
    FundamentusHTMLParserAdapter
)
from app.src.features.get_b3_stock_tickers.infra.repositories.dynamodb_database_repository import (
    DynamoDBDatabaseRepository
)
from app.src.features.get_b3_stock_tickers.infra.adapters.sqs_queue_adapter import SQSQueueAdapter
from app.src.features.get_b3_stock_tickers.infra.adapters.sns_topic_adapter import SNSTopicAdapter
from app.src.features.get_b3_stock_tickers.infra.mappers.http_response_mapper import HTTPResponseMapper



# Initializing mappers, adapters and repositories
http_client_adapter = RequestsHTTPClientAdapter()
html_parser_adapter = FundamentusHTMLParserAdapter()
database_repository = DynamoDBDatabaseRepository()
queue_adapter = SQSQueueAdapter()
topic_adapter = SNSTopicAdapter()


# Initializing use case
use_case = GetB3StockTickersUseCase(
    http_client_adapter=http_client_adapter,
    html_parser_adapter=html_parser_adapter,
    database_repository=database_repository,
    queue_adapter=queue_adapter,
    topic_adapter=topic_adapter
)


# Defining a handler function for executing the use case in AWS Lambda
def handler(event: dict[str, Any], context: Any) -> Any:
    """
    AWS Lambda handler function to execute the GetB3StockTickersUseCase.

    Args:
        event (dict[str, Any]): The event data passed to the Lambda function.
        context (Any): The context object provided by AWS Lambda.

    Returns:
        Any: The result of the use case execution, typically a list of stock tickers.
    """

    output_dto = use_case.execute()

    return HTTPResponseMapper.map(output_dto)
