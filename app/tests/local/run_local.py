from dotenv import find_dotenv, load_dotenv

from app.src.features.get_investment_portfolios.presentation import get_investment_portfolios_presentation
from app.src.features.store_dynamodb_streams_data.presentation import store_dynamodb_streams_data_presentation
from app.src.features.get_active_stocks.presentation import get_active_stocks_presentation
from app.src.features.get_fundamentus_eod_stock_metrics.presentation import get_fundamentus_eod_stock_metrics_presentation

from app.tests.mocks.mocked_input_events import (
    MOCKED_DYNAMODB_STREAMS_EVENT,
    MOCKED_SQS_EVENT
)


# Loading environment variables from .env file
_ = load_dotenv(find_dotenv())

# Building handlers
get_investment_portfolios_handler = get_investment_portfolios_presentation.handler
store_dynamodb_streams_data_handler = store_dynamodb_streams_data_presentation.handler
get_active_stocks_handler = get_active_stocks_presentation.handler
get_fundamentus_eod_stock_metrics_handler = get_fundamentus_eod_stock_metrics_presentation.handler

"""
FEATURE: Get Investment Portfolio

DESCRIPTION:
    This feature provides functionality retrieve investment portfolio data from
    a given source defined by users through a adapter (e.g., S3, Google Drive, APIs).
"""
# response = get_investment_portfolios_handler(event=None, context=None)
# print(response)


"""
FEATURE: Store DynamoDB Streams Data

DESCRIPTION:
    This feature provides functionality to stream data from DynamoDB and process it in real-time.
"""
# response = store_dynamodb_streams_data_handler(event=MOCKED_DYNAMODB_STREAMS_EVENT, context=None)
# print(response)


"""
FEATURE: Get Active Stocks

DESCRIPTION:
    This feature provides functionality to scrape and retrieve active stock data from
    a web site (e.g., Fundamentus) and process it for further use.
"""
# response = get_active_stocks_handler(event=None, context=None)
# print(response)


"""
FEATURE: Get Fundamentus EOD Stock Metrics

DESCRIPTION:
    This feature provides functionality to scrape and retrieve end-of-day stock metrics from
    the Fundamentus investment website and process it for further use.
"""
response = get_fundamentus_eod_stock_metrics_handler(event=MOCKED_SQS_EVENT, context=None)
# print(response)

# TODO: Take a look at the __parse_float_cols method on the HTML parser adapter to handle