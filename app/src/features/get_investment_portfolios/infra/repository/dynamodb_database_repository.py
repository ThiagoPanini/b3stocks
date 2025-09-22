import os
from typing import Any

import boto3
from pynamodb.models import Model
from pynamodb.attributes import (
    UnicodeAttribute,
    JSONAttribute
)
from pynamodb.exceptions import DoesNotExist

from app.src.features.get_investment_portfolios.domain.interfaces.database_repository_interface import (
    IDatabaseRepository
)
from app.src.features.get_investment_portfolios.domain.entities.investment_portfolio import (
    InvestmentPortfolio
)

from app.src.features.cross.utils.log import LogUtils
from app.src.features.cross.utils.serialization import SerializationUtils
from app.src.features.cross.utils.decorators import timing_decorator


class InvestmentPortfolioModel(Model):
    """
    PynamoDB model for investment portfolio.
    """
    class Meta:
        table_name = os.getenv("DYNAMODB_INVESTMENT_PORTFOLIO_TABLE_NAME")
        region = boto3.session.Session().region_name

    owner_name = UnicodeAttribute()
    owner_mail = UnicodeAttribute(hash_key=True)
    stocks = JSONAttribute()
    source_url = UnicodeAttribute(null=True)
    created_at = UnicodeAttribute()
    updated_at = UnicodeAttribute()

    def __init__(self, *args, **kwargs):
        self.Meta.table_name = os.getenv("DYNAMODB_INVESTMENT_PORTFOLIO_TABLE_NAME")
        super().__init__(*args, **kwargs)


class DynamoDBDatabaseRepository(IDatabaseRepository):
    """
    Implementation of the investment portfolio repository using DynamoDB.
    """

    def __init__(self):
        self.logger = LogUtils.setup_logger(name=__name__)


    @timing_decorator(enabled=True)
    def save_items(self, items: list[InvestmentPortfolio]) -> None:
        """
        Saves a list of investment portfolio data to the database repository.

        Args:
            items (list[InvestmentPortfolio]): The investment portfolio data to save.
        """

        for item in items:
            # Tries to update the item if it already exists (based on the hash key)
            serialized_item = SerializationUtils.json_serialize(item)

            try:
                # Getting item if already exists and preserve created_at
                existing_item = InvestmentPortfolioModel.get(serialized_item["owner_mail"])

                # Update only mutable fields
                existing_item.update(
                    actions=[
                        InvestmentPortfolioModel.owner_name.set(serialized_item["owner_name"]),
                        InvestmentPortfolioModel.stocks.set(serialized_item["stocks"]),
                        InvestmentPortfolioModel.source_url.set(serialized_item["source_url"]),
                        InvestmentPortfolioModel.updated_at.set(serialized_item["updated_at"])
                    ]
                )

            except DoesNotExist:
                # If item does not exist, create a new one    
                try:
                    InvestmentPortfolioModel(**serialized_item).save()

                except Exception:
                    self.logger.exception("Failed to save investment portfolio to DynamoDB for "
                                          f"hash_key={serialized_item['owner_mail']}")
                    raise
