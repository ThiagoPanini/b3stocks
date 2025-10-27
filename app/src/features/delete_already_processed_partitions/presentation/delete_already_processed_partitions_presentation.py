from typing import Any

from app.src.features.delete_already_processed_partitions.infra.adapters.awsrangler_data_catalog_adapter import (
    AWSRanglerDataCatalogAdapter
)
from app.src.features.delete_already_processed_partitions.use_case.delete_already_processed_partitions_use_case import (
    DeleteAlreadyProcessedPartitionsUseCase
)
from app.src.features.cross.infra.mappers.http_response_mapper import HTTPResponseMapper
from app.src.features.cross.utils.env import EnvironmentVarsUtils

# Initializing mappers, adapters and repositories
data_catalog_adapter = AWSRanglerDataCatalogAdapter()

# Initializing the use case
use_case = DeleteAlreadyProcessedPartitionsUseCase(
    data_catalog_adapter=data_catalog_adapter
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
    output_dto = use_case.execute()

    return HTTPResponseMapper.map(output_dto)
