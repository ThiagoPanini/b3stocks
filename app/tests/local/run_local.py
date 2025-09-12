from dotenv import find_dotenv, load_dotenv

from app.src.features.get_investment_portfolio.presentation import get_investment_portfolio_presentation
from app.src.features.stream_cdc_data.presentation import stream_cdc_data_presentation

from app.tests.mocks.mocked_input_events import MOCKED_DYNAMODB_STREAM_EVENT


# Loading environment variables from .env file
_ = load_dotenv(find_dotenv())

# Building handlers
get_investment_portfolio_handler = get_investment_portfolio_presentation.handler
stream_cdc_data_handler = stream_cdc_data_presentation.handler

"""
FEATURE: Get Investment Portfolio

DESCRIPTION:
    This feature provides functionality to scrape and retrieve investment portfolio data from
    a given source defined by users through a adapter (e.g., S3, Google Drive, APIs).
"""

response = get_investment_portfolio_handler(event=None, context=None)
print(response)


"""
FEATURE: Stream DynamoDB Data

DESCRIPTION:
    This feature provides functionality to stream data from DynamoDB and process it in real-time.
"""

response = stream_cdc_data_handler(event=MOCKED_DYNAMODB_STREAM_EVENT, context=None)
print(response)
