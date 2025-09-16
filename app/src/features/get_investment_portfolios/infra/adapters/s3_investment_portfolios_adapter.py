import os
import yaml

import boto3

from app.src.features.get_investment_portfolios.domain.interfaces.investment_portfolio_adapter_interface import (
    IInvestmentPortfolioAdapter
)
from app.src.features.get_investment_portfolios.domain.entities import (
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
        self.bucket_name_prefix = os.getenv("S3_ARTIFACTS_BUCKET_NAME_PREFIX")
        self.portfolios_key_prefix = os.getenv("S3_INVESTMENT_PORTFOLIOS_KEY_PREFIX")
        self.bucket_name = self.__build_bucket_name()


    def __build_bucket_name(self) -> str:
        """
        Constructs the S3 bucket name using the prefix, account ID and AWS region.

        Returns:
            The constructed S3 bucket name.
        """
        region = boto3.session.Session().region_name
        account_id = boto3.client("sts").get_caller_identity().get("Account")

        return f"{self.bucket_name_prefix}-{account_id}-{region}"

    
    def fetch_portfolio(self) -> list[InvestmentPortfolio]:
        """
        Fetch and parse the investment portfolio YAML stored in S3.

        Returns:
            list[InvestmentPortfolio]:
                A list of InvestmentPortfolio instances containing, each one, an individual
                portfolio data.
        """
        if not self.bucket_name_prefix or not self.portfolios_key_prefix:
            raise ValueError("Environment variables S3_ARTIFACTS_BUCKET_NAME_PREFIX and "
                             "S3_INVESTMENT_PORTFOLIOS_KEY_PREFIX must be set")

        # List all objects under the portfolios key prefix
        try:
            paginator = self.client.get_paginator("list_objects_v2")
            page_iterator = paginator.paginate(
                Bucket=self.bucket_name,
                Prefix=self.portfolios_key_prefix
            )

            portfolios_objects_keys = []
            for page in page_iterator:
                for obj in page.get("Contents", []):
                    if obj.get("Key").endswith(".yaml") or obj.get("Key").endswith(".yml"):
                        portfolios_objects_keys.append(obj.get("Key"))
        
        except self.client.exceptions.NoSuchBucket:
            self.logger.exception(f"S3 bucket {self.bucket_name} does not exist.")
            raise

        except Exception:
            self.logger.exception("Error listing portfolio objects in S3")
            raise

        # Iterate over each portfolio object and fetch/parse it
        investment_portfolios: list[InvestmentPortfolio] = []
        for object_key in portfolios_objects_keys:
            try:
                response = self.client.get_object(Bucket=self.bucket_name, Key=object_key)
                raw_content = response["Body"].read().decode("utf-8")

            except self.client.exceptions.NoSuchKey:
                self.logger.exception(f"Object key {object_key} not found in bucket {self.bucket_name}")
                raise

            except Exception:
                self.logger.exception(f"Error fetching portfolio object {object_key} from S3")
                raise

            # Parse raw content into a structured yaml file object
            try:
                parsed = yaml.safe_load(raw_content)

            except yaml.YAMLError:
                self.logger.exception(f"Failed to parse YAML portfolio file {object_key}")
                raise

            if not parsed or "portfolio" not in parsed:
                raise ValueError("Invalid portfolio YAML: missing 'portfolio' root key")

            # Get portfolio details
            portfolio_data = parsed["portfolio"]
            owner_name = portfolio_data.get("owner")
            owner_mail = portfolio_data.get("email")
            stocks_data = portfolio_data.get("stocks")

            if not owner_name or not owner_mail:
                raise ValueError("Portfolio owner name and email must be provided in YAML")

            # Parse stocks data
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
                source_url=f"s3://{self.bucket_name}/{object_key}"
            )

            investment_portfolios.append(portfolio)

        return investment_portfolios
