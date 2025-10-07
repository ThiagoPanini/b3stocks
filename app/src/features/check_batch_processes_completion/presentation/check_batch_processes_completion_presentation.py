from typing import Any

from app.src.features.check_batch_processes_completion.use_case.check_batch_processes_completion_use_case import (
    CheckBatchProcessesCompletionUseCase
)
from app.src.features.cross.infra.mappers.dynamodb_streams_lambda_event_mapper import (
    DynamoDBStreamsLambdaEventMapper
)
from app.src.features.check_batch_processes_completion.infra.adapters.sns_topic_adapter import (
    SNSTopicAdapter
)
from app.src.features.cross.infra.mappers.http_response_mapper import HTTPResponseMapper
from app.src.features.cross.utils.env import EnvironmentVarsUtils


# Initialize mappers, adapters and repositories
event_mapper = DynamoDBStreamsLambdaEventMapper()
topic_adapter = SNSTopicAdapter()

# Initializing use case
use_case = CheckBatchProcessesCompletionUseCase(
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
        dict: The result of the use case execution.
    """

    EnvironmentVarsUtils.check_required_env_vars(
        required_env_vars=[
            "SNS_BATCH_PROCESSES_COMPLETION_TOPIC_NAME"
        ]
    )

    input_dto = event_mapper.map_event_to_input_dto(event=event)
    output_dto = use_case.execute(input_dto=input_dto)

    return HTTPResponseMapper.map(output_dto)