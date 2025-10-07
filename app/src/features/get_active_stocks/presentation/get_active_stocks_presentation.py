from typing import Any

from app.src.features.cross.infra.adapters.requests_http_client_adapter import (
    RequestsHTTPClientAdapter
)
from app.src.features.get_active_stocks.infra.adapters.fundamentus_html_parser_adapter import (
    FundamentusHTMLParserAdapter
)
from app.src.features.get_active_stocks.infra.repositories.dynamodb_database_repository import (
    DynamoDBDatabaseRepository
)
from app.src.features.get_active_stocks.infra.adapters.sns_topic_adapter import SNSTopicAdapter
from app.src.features.get_active_stocks.use_case.get_active_stocks_use_case import (
    GetActiveStocksUseCase
)
from app.src.features.cross.infra.mappers.http_response_mapper import HTTPResponseMapper
from app.src.features.cross.utils.env import EnvironmentVarsUtils


# Initializing mappers, adapters and repositories
http_client_adapter = RequestsHTTPClientAdapter()
html_parser_adapter = FundamentusHTMLParserAdapter()
database_repository = DynamoDBDatabaseRepository()
topic_adapter = SNSTopicAdapter()

# Initializing the use case
use_case = GetActiveStocksUseCase(
    http_client_adapter=http_client_adapter,
    html_parser_adapter=html_parser_adapter,
    database_repository=database_repository,
    topic_adapter=topic_adapter
)


# Defining a handler function for executing the use case in AWS Lambda
def handler(event: dict[str, Any], context: Any = None) -> dict:
    """
    AWS Lambda handler function to execute the use case.

    Args:
        event (dict[str, Any]): The event data passed to the Lambda function.
        context (Any): The context object provided by AWS Lambda.

    Returns:
        dict: The result of the use case execution, typically a B3InvestmentPortfolioRequest instance.
    """

    EnvironmentVarsUtils.check_required_env_vars(
        required_env_vars=[
            "DYNAMODB_ACTIVE_STOCKS_TABLE_NAME",
            "SNS_ACTIVE_STOCKS_TOPIC_NAME"
        ]
    )

    output_dto = use_case.execute()

    return HTTPResponseMapper.map(output_dto)
