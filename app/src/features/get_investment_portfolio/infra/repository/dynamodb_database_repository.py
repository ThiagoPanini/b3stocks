import os
import boto3
from pynamodb.models import Model
from pynamodb.attributes import (
    UnicodeAttribute,
    JSONAttribute
)

from app.src.features.get_investment_portfolio.domain.interfaces.database_repository_interface import (
    IDatabaseRepository
)
from app.src.features.get_investment_portfolio.domain.entities.investment_portfolio import (
    InvestmentPortfolio
)

from app.src.features.cross.utils.log_utils import setup_logger
from app.src.features.cross.utils.serialization_utils import entity_to_storage_dict


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
        self.logger = setup_logger(__name__)


    def put_item(self, item: InvestmentPortfolio) -> None:
        """
        Saves an investment portfolio data into a DynamoDB table.

        Args:
            item (InvestmentPortfolio): The investment portfolio to save.
        """

        try:
            data = entity_to_storage_dict(item)

        except Exception as e:
            self.logger.exception("Failed to serialize investment portfolio data to JSON")
            raise e

        try:
            InvestmentPortfolioModel(
                owner_name=data["owner_name"],
                owner_mail=data["owner_mail"],
                stocks=data["stocks"],
                created_at=data["created_at"],
                updated_at=data["updated_at"],
            ).save()

        except Exception as e:
            self.logger.exception("Failed to save investment portfolio to DynamoDB")
            raise e