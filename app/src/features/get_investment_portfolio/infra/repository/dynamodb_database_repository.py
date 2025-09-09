import os
import boto3
from pynamodb.models import Model
from pynamodb.attributes import (
    UnicodeAttribute,
    JSONAttribute
)
from pynamodb.exceptions import DoesNotExist

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
        self.logger = setup_logger(__name__)

    
    def __serialize_item(self, item: InvestmentPortfolio) -> dict:
        """
        Serializes an InvestmentPortfolio entity to a dictionary suitable for storage.

        Args:
            item (InvestmentPortfolio): The investment portfolio to update.

        Returns:
            dict: The serialized investment portfolio data.
        """

        try:
            data = entity_to_storage_dict(item)
            return data

        except Exception as e:
            self.logger.exception("Failed to serialize investment portfolio data to JSON")
            raise e


    def save_item(self, item: InvestmentPortfolio) -> None:
        """
        Saves an investment portfolio data into a DynamoDB table.

        Args:
            item (InvestmentPortfolio): The investment portfolio to save.
        """

        # Tries to update the item if it already exists (based on the hash key)
        try:
            data = self.__serialize_item(item)

            # Getting item if already exists and preserve created_at
            existing_item = InvestmentPortfolioModel.get(data["owner_mail"])

            # Update only muttable fields
            existing_item.update(
                actions=[
                    InvestmentPortfolioModel.owner_name.set(data["owner_name"]),
                    InvestmentPortfolioModel.stocks.set(data["stocks"]),
                    InvestmentPortfolioModel.source_url.set(data["source_url"]),
                    InvestmentPortfolioModel.updated_at.set(data["updated_at"])
                ]
            )
            self.logger.info("Successfully updated existent investment portfolio in DynamoDB "
                        f"for hash_key={data['owner_mail']}")

        except DoesNotExist:
            # If item does not exist, create a new one    
            try:
                InvestmentPortfolioModel(**data).save()

                self.logger.info("Successfully created a new investment portfolio in DynamoDB "
                            f"for hash_key={data['owner_mail']}")

            except Exception as e:
                self.logger.exception("Failed to save investment portfolio to DynamoDB")
                raise e
