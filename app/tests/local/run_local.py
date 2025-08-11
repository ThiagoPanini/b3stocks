from dotenv import find_dotenv, load_dotenv
from app.src.features.get_b3_stock_tickers.presentation import get_b3_stock_tickers_presentation


# Loading environment variables from .env file
_ = load_dotenv(find_dotenv())

# Building handlers
get_b3_stock_tickers_handler = get_b3_stock_tickers_presentation.handler


"""
FEATURE: Get B3 Stock Tickers

DESCRIPTION:
    This feature provides functionality to scrape and retrieve stock tickers from the B3 (Brazilian
    Stock Exchange) using a web scraping adapter.
"""

response = get_b3_stock_tickers_handler(event=None, context=None)
print(response)
