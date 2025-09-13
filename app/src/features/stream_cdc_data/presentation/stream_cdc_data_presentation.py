from typing import Any

from app.src.features.stream_cdc_data.infra.mappers.lambda_event_mapper import LambdaEventMapper
from app.src.features.stream_cdc_data.infra.adapters.awswrangler_data_catalog_sync_adapter import (
    AWSWranglerDataCatalogSyncAdapter
)
from app.src.features.stream_cdc_data.use_case.stream_cdc_data_use_case import (
    StreamCDCDataUseCase
)
from app.src.features.cross.infra.mappers.http_response_mapper import HTTPResponseMapper


# Initialize mappers, adapters and repositories
event_mapper = LambdaEventMapper()
data_catalog_sync_adapter = AWSWranglerDataCatalogSyncAdapter()

# Build the use case
use_case = StreamCDCDataUseCase(
    data_catalog_sync_adapter=data_catalog_sync_adapter
)


# Defining a handler function for executing the use case in AWS Lambda
def handler(event: dict[str, Any], context: Any = None) -> dict:
    """
    AWS Lambda handler function to execute the GetInvestmentPortfolioUseCase.

    Args:
        event (dict): The event data passed to the Lambda function.
        context (Any): The context object provided by AWS Lambda.

    Returns:
        dict: The result of the use case execution, typically a B3InvestmentPortfolioRequest instance.
    """

    input_dto = event_mapper.map_event_to_input_dto(event=event)
    output_dto = use_case.execute(input_dto=input_dto)

    return HTTPResponseMapper.map(output_dto)
