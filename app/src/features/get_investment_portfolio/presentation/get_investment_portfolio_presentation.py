from typing import Any

from app.src.features.get_investment_portfolio.infra.adapters.s3_investment_portfolio_request_adapter import (
    S3InvestmentPortfolioRequestAdapter
)
from app.src.features.get_investment_portfolio.use_case.get_investment_portfolio_use_case import (
    GetInvestmentPortfolioUseCase
)
from app.src.features.cross.infra.mappers.http_response_mapper import HTTPResponseMapper


# Initializing mappers, adapters and repositories
s3_investment_portfolio_request_adapter = S3InvestmentPortfolioRequestAdapter()


# Initializing use case
use_case = GetInvestmentPortfolioUseCase(
    investment_portfolio_request_adapter=s3_investment_portfolio_request_adapter
)

# Defining a handler function for executing the use case in AWS Lambda
def handler(event: dict, context: dict) -> dict:
    """
    AWS Lambda handler function to execute the GetInvestmentPortfolioUseCase.

    Args:
        event (dict): The event data passed to the Lambda function.
        context (dict): The context object provided by AWS Lambda.

    Returns:
        dict: The result of the use case execution, typically a B3InvestmentPortfolioRequest instance.
    """

    output_dto = use_case.execute()

    return HTTPResponseMapper.map(output_dto)