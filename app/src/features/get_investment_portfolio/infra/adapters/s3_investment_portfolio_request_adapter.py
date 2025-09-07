import os

import boto3
import io
import csv
from uuid import uuid4

from app.src.features.get_investment_portfolio.domain.entities.b3_investment_portfolio_request import (
    B3InvestmentPortfolioRequest
)
from app.src.features.get_investment_portfolio.domain.interfaces.investment_portfolio_request_adapter_interface import (
    IInvestmentPortfolioRequestAdapter
)
from app.src.features.get_investment_portfolio.domain.entities.b3_stock import B3Stock
from app.src.features.cross.utils.log_utils import setup_logger


class S3InvestmentPortfolioRequestAdapter(IInvestmentPortfolioRequestAdapter):
    """
    Adapter for fetching investment portfolio data from S3.
    """

    def __init__(self):
        self.logger = setup_logger(name=__name__)
        self.client = boto3.client("s3", region_name=boto3.session.Session().region_name)
        self.bucket_name = os.getenv("S3_B3STOCKS_ARTIFACT_BUCKET_NAME")
        self.object_key = os.getenv("S3_INVESTMENT_PORTFOLIO_OBJECT_KEY")

    def fetch_portfolio(self) -> B3InvestmentPortfolioRequest:
        """
        Fetches the investment portfolio data from S3.

        Returns:
            B3InvestmentPortfolioRequest: An instance of B3InvestmentPortfolioRequest containing the portfolio data.
        """

        try:
            # Getting the object from S3
            response = self.client.get_object(
                Bucket=self.bucket_name,
                Key=self.object_key
            )
            content = response['Body'].read().decode("utf-8-sig")

            # Reading file using csv reader
            csv_file = io.StringIO(content)
            csv_reader = csv.reader(csv_file, delimiter=";")

            # Get headers to skip them
            _ = next(csv_reader, None)

            stocks = []
            for line_number, row in enumerate(csv_reader, start=1):
                # Skip header or empty lines
                if not row or len(row) < 4 or not row[1].strip():
                    self.logger.debug(f"Skipping invalid or empty row at line {line_number}: {row}")
                    continue

                try:
                    product_name = row[0].strip() or None
                    stock_code = row[1].strip()
                    company_cnpj = row[2].strip() or None
                    isin_code = row[3].strip() or None

                    stock = B3Stock(
                        stock_code=stock_code,
                        product_name=product_name,
                        company_cnpj=company_cnpj,
                        isin_code=isin_code,
                    )
                    stocks.append(stock)

                except Exception as e:
                    self.logger.exception(f"Error parsing row {line_number}: {row}")
                    raise e

            return B3InvestmentPortfolioRequest(
                request_id=str(uuid4()),
                source_url=f"s3://{self.bucket_name}/{self.object_key}",
                stocks_list=stocks,
            )

        except self.client.exceptions.NoSuchKey:
            self.logger.exception(f"CSV file {self.object_key} not found in bucket {self.bucket_name}")
            raise

        except Exception as e:
            self.logger.exception("Unexpected error while fetching portfolio from S3")
            raise
