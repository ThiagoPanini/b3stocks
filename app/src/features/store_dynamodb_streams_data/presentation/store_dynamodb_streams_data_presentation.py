from typing import Any

from app.src.features.cross.infra.mappers.dynamodb_streams_lambda_event_mapper import (
    DynamoDBStreamsLambdaEventMapper
)
from app.src.features.cross.infra.adapters.awswrangler_cdc_data_catalog_sync_adapter import (
    AWSWranglerCDCDataCatalogSyncAdapter
)
from app.src.features.store_dynamodb_streams_data.use_case.store_dynamodb_streams_data_use_case import (
    StoreDynamoDBStreamsDataUseCase
)
from app.src.features.cross.infra.mappers.http_response_mapper import HTTPResponseMapper
from app.src.features.cross.utils.env import EnvironmentVarsUtils


# Initialize mappers, adapters and repositories
event_mapper = DynamoDBStreamsLambdaEventMapper()
cdc_data_catalog_sync_adapter = AWSWranglerCDCDataCatalogSyncAdapter()

# Build the use case
use_case = StoreDynamoDBStreamsDataUseCase(
    cdc_data_catalog_sync_adapter=cdc_data_catalog_sync_adapter
)


# Defining a handler function for executing the use case in AWS Lambda
def handler(event: dict[str, Any], context: Any = None) -> dict[str, Any]:
    """
    AWS Lambda handler function to execute the feature use case.
    
    It's important to mention that this source code can be used by multiple Lambda functions that
    need to store and sync data from a DynamoDB Streams source with a data catalog. The code can
    be reused by different Lambda functions by configuring the appropriate triggers and
    environment variables for each function.

    Args:
        event (dict): The event data passed to the Lambda function.
        context (Any): The context object provided by AWS Lambda.

    Returns:
        dict[str, Any]: The result of the use case execution.
    """

    EnvironmentVarsUtils.check_required_env_vars(
        required_env_vars=[
            "S3_ANALYTICS_CDC_BUCKET_NAME_PREFIX",
            "S3_ANALYTICS_SOR_BUCKET_NAME_PREFIX",
            "DATA_CATALOG_CDC_DATABASE_NAME",
            "DATA_CATALOG_SOR_DATABASE_NAME"
        ]
    )

    input_dto = event_mapper.map_event_to_input_dto(event=event)
    output_dto = use_case.execute(input_dto=input_dto)

    return HTTPResponseMapper.map(output_dto)
