from typing import Any

from app.src.features.get_fundamentus_eod_stock_metrics.use_case.get_fundamentus_eod_stock_metrics_use_case import (
    GetFundamentusEodStockMetricsUseCase
)
from app.src.features.cross.infra.mappers.http_response_mapper import HTTPResponseMapper


# Initializing mappers, adapters and repositories


# Initializing use case
use_case = GetFundamentusEodStockMetricsUseCase()


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

    output_dto = use_case.execute()

    return HTTPResponseMapper.map(output_dto)