from typing import Any

from app.src.features.get_fundamentus_eod_stock_metrics.infra.mappers.sqs_messages_lambda_event_mapper import (
    SQSMessagesLambdaEventMapper
)
from app.src.features.get_fundamentus_eod_stock_metrics.infra.adapters.fundamentus_html_parser_adapter import (
    FundamentusHTMLParserAdapter
)
from app.src.features.get_fundamentus_eod_stock_metrics.infra.repositories.dynamodb_database_repository import (
    DynamoDBDatabaseRepository
)
from app.src.features.get_fundamentus_eod_stock_metrics.use_case.get_fundamentus_eod_stock_metrics_use_case import (
    GetFundamentusEodStockMetricsUseCase
)

from app.src.features.cross.infra.adapters.requests_http_client_adapter import RequestsHTTPClientAdapter
from app.src.features.cross.infra.mappers.http_response_mapper import HTTPResponseMapper
from app.src.features.cross.infra.repositories.dynamodb_batch_control_database_repository import (
    DynamoDBBatchControlDatabaseRepository
)
from app.src.features.cross.utils.env import EnvironmentVarsUtils


# Initializing mappers, adapters and repositories
event_mapper = SQSMessagesLambdaEventMapper()
http_client_adapter = RequestsHTTPClientAdapter()
html_parser_adapter = FundamentusHTMLParserAdapter()
database_repository = DynamoDBDatabaseRepository()
batch_control_database_repository = DynamoDBBatchControlDatabaseRepository()

# Initializing use case
use_case = GetFundamentusEodStockMetricsUseCase(
    http_client_adapter=http_client_adapter,
    html_parser_adapter=html_parser_adapter,
    database_repository=database_repository,
    batch_control_database_repository=batch_control_database_repository
)


# Defining a handler function for executing the use case in AWS Lambda
def handler(event: dict[str, Any], context: Any = None) -> dict:
    """
    AWS Lambda handler function to execute the use case.

    Args:
        event (dict[str, Any]): The event data passed to the Lambda function.
        context (Any): The context object provided by AWS Lambda.

    Returns:
        dict: The result of the use case execution.
    """

    EnvironmentVarsUtils.check_required_env_vars(
        required_env_vars=[
            "DYNAMODB_FUNDAMENTUS_EOD_STOCK_METRICS_TABLE_NAME",
            "DYNAMODB_BATCH_PROCESS_CONTROL_TABLE_NAME"
        ]
    )

    input_dto = event_mapper.map_event_to_input_dto(event=event)
    output_dto = use_case.execute(input_dto=input_dto)

    return HTTPResponseMapper.map(output_dto)