import os
import yaml

import boto3

from app.src.features.get_investment_portfolio.domain.interfaces.investment_portfolio_adapter_interface import (
    IInvestmentPortfolioAdapter
)
from app.src.features.get_investment_portfolio.domain.entities import (
    InvestmentPortfolio,
    StockVariationControl,
    VariationThreshold
)
from app.src.features.cross.utils.log_utils import setup_logger


class S3InvestmentPortfolioAdapter(IInvestmentPortfolioAdapter):
    """
    Adapter for fetching investment portfolio data from S3.
    """

    def __init__(self):
        self.logger = setup_logger(name=__name__)
        self.client = boto3.client("s3", region_name=boto3.session.Session().region_name)
        self.bucket_name = os.getenv("S3_ARTIFACT_BUCKET_NAME")
        self.object_key = os.getenv("S3_INVESTMENT_PORTFOLIO_OBJECT_KEY")

    def __build_source_url(self) -> str:
        """
        Constructs the S3 URL for the investment portfolio object.

        Returns:
            Optional[str]: The S3 URL if bucket and object key are set, otherwise None.
        """
        return f"s3://{self.bucket_name}/{self.object_key}"

    
    def fetch_portfolio(self) -> InvestmentPortfolio:
        """
        Fetch and parse the investment portfolio YAML stored in S3.

        Expected YAML structure:
        portfolio:
          owner: str
          email: str
          stocks:
            - name: str
              ticker: str
              notify_on_threshold: bool
              variation_thresholds:
                upper_bound: float
                lower_bound: float
        """

        if not self.bucket_name or not self.object_key:
            raise ValueError("Environment variables S3_ARTIFACT_BUCKET_NAME and S3_INVESTMENT_PORTFOLIO_OBJECT_KEY must be set")

        try:
            response = self.client.get_object(Bucket=self.bucket_name, Key=self.object_key)
            raw_content = response["Body"].read().decode("utf-8")

            # Parse YAML
            try:
                parsed = yaml.safe_load(raw_content)

            except yaml.YAMLError:
                self.logger.exception("Failed to parse YAML portfolio file")
                raise

            if not parsed or "portfolio" not in parsed:
                raise ValueError("Invalid portfolio YAML: missing 'portfolio' root key")

            portfolio_data = parsed["portfolio"]
            owner_name = portfolio_data.get("owner")
            owner_mail = portfolio_data.get("email")
            stocks_data = portfolio_data.get("stocks")

            if not owner_name or not owner_mail:
                raise ValueError("Portfolio owner name and email must be provided in YAML")

            stocks: list[StockVariationControl] = []

            for idx, stock_item in enumerate(stocks_data, start=1):
                try:
                    stock_variation_control = StockVariationControl(
                        company_name=stock_item["name"],
                        ticker_code=stock_item["ticker"],
                        stock_type=None,  # Derived in __post_init__
                        notify_on_threshold=bool(stock_item["notify_on_threshold"]),
                        variation_thresholds=VariationThreshold(
                            upper_bound=float(stock_item["variation_thresholds"]["upper_bound"]),
                            lower_bound=float(stock_item["variation_thresholds"]["lower_bound"]),
                        )
                    )
                    stocks.append(stock_variation_control)

                except Exception:
                    self.logger.exception(f"Error parsing stock entry at index {idx}: {stock_item}")
                    raise

            portfolio = InvestmentPortfolio(
                owner_name=owner_name,
                owner_mail=owner_mail,
                stocks=stocks,
                source_url=self.__build_source_url()
            )

            return portfolio

        except self.client.exceptions.NoSuchBucket:
            self.logger.exception(f"S3 bucket {self.bucket_name} does not exist.")
            raise

        except self.client.exceptions.NoSuchKey:
            self.logger.exception(f"Object key {self.object_key} not found in bucket {self.bucket_name}")
            raise

        except Exception:
            self.logger.exception("Unexpected error while fetching/parsing portfolio from S3")
            raise
