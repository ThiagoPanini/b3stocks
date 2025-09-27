from typing import Any

from app.src.features.check_batch_processes_completion.use_case.check_batch_processes_completion_use_case import (
    CheckBatchProcessesCompletionUseCase
)
from app.src.features.cross.infra.mappers.dynamodb_streams_lambda_event_mapper import (
    DynamoDBStreamsLambdaEventMapper
)
from app.src.features.cross.infra.mappers.http_response_mapper import HTTPResponseMapper



# Initialize mappers, adapters and repositories
event_mapper = DynamoDBStreamsLambdaEventMapper()


# Initializing use case
use_case = CheckBatchProcessesCompletionUseCase()


# Defining a handler function for executing the use case in AWS Lambda
def handler(event: dict[str, Any], context: Any = None) -> dict:
    """
    AWS Lambda handler function to execute the GetInvestmentPortfolioUseCase.

    Args:
        event (dict[str, Any]): The event data passed to the Lambda function.
        context (Any): The context object provided by AWS Lambda.

    Returns:
        dict: The result of the use case execution, typically a B3InvestmentPortfolioRequest instance.
    """

    input_dto = event_mapper.map_event_to_input_dto(event=event)
    output_dto = use_case.execute(input_dto=input_dto)

    return HTTPResponseMapper.map(output_dto)