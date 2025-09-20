import os

import boto3
from pynamodb.models import Model
from pynamodb.attributes import (
    UnicodeAttribute,
    MapAttribute
)

from app.src.features.cross.utils.log_utils import setup_logger, log_loop_status
from app.src.features.cross.utils.decorators import timing_decorator
from app.src.features.cross.utils.serialization import json_serialize

from app.src.features.get_active_stocks.domain.interfaces.database_repository_interface import (
    IDatabaseRepository
)
from app.src.features.get_active_stocks.domain.entities.stock import Stock


class StockModel(Model):
    """
    PynamoDB model for stock data.
    """
    class Meta:
        table_name = os.getenv("DYNAMODB_ACTIVE_STOCKS_TABLE_NAME")
        region = boto3.session.Session().region_name

    code = UnicodeAttribute(hash_key=True)
    company_name = UnicodeAttribute(null=True)
    request_config = MapAttribute()
    created_at = UnicodeAttribute()
    updated_at = UnicodeAttribute()

    def __init__(self, *args, **kwargs):
        self.Meta.table_name = os.getenv("DYNAMODB_ACTIVE_STOCKS_TABLE_NAME")
        super().__init__(*args, **kwargs)


class DynamoDBDatabaseRepository(IDatabaseRepository):
    """
    Implementation of the B3 stock tickers repository using DynamoDB.
    """
    def __init__(self):
        self.logger = setup_logger(__name__)


    @timing_decorator
    def batch_insert_items(self, items: list[Stock]) -> None:
        """
        Inserts a batch of stocks to the repository.

        Args:
            items (list[Stock]): The list of stocks to insert.
        """
        # Getting company name with None to debugging purposes
        for item in items:
            if item.company_name is None:
                self.logger.warning(f"Company name is None for stock code {item.code}")

        try:
            with StockModel.batch_write() as batch:
                for idx, stock in enumerate(items):
                    model = (StockModel(**json_serialize(stock)))
                    batch.save(model)

                    # Logging the status of the loop
                    log_loop_status(
                        logger=self.logger,
                        loop_idx=idx,
                        total_elements=len(items),
                        log_pace=200,
                        log_msg=f"Put {idx} items to the database repository"
                    )

        except Exception:
            self.logger.exception("Error saving batch of stocks data on table "
                                  f"{StockModel.Meta.table_name} on stock {stock}")
            raise
        else:
            self.logger.info("Successfully inserted items to DynamoDB table "
                             f"{StockModel.Meta.table_name}")
