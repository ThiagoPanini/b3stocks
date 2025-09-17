import os

import boto3
import awswrangler as wr
import pandas as pd

from app.src.features.cross.utils.log_utils import setup_logger
from app.src.features.cross.domain.interfaces.cdc_data_catalog_sync_adapter_interface import (
    ICDCDataCatalogSyncAdapter
)
from app.src.features.cross.domain.entities.dynamodb_streams_output_data import (
    DynamoDBStreamsOutputData
)


class AWSWranglerCDCDataCatalogSyncAdapter(ICDCDataCatalogSyncAdapter):
    """
    Implementation of ICDCDataCatalogSyncAdapter to store and sync from a database streams source
    with a catalog using AWS Wrangler.
    """

    def __init__(self):
        self.logger = setup_logger(name=__name__)
        self.bucket_name_prefix = os.getenv("S3_ANALYTICS_CDC_BUCKET_NAME_PREFIX")
        self.bucket_name = self.__build_bucket_name()
        self.data_catalog_database = os.getenv("DATA_CATALOG_CDC_DATABASE_NAME")


    def __build_bucket_name(self) -> str:
        """
        Constructs the S3 bucket name using the prefix, account ID and AWS region.

        Returns:
            The constructed S3 bucket name.
        """
        region = boto3.session.Session().region_name
        account_id = boto3.client("sts").get_caller_identity().get("Account")

        return f"{self.bucket_name_prefix}-{account_id}-{region}"


    def store_and_sync_cdc_data(self, data: list[DynamoDBStreamsOutputData]) -> None:
        """
        Adapter to store data in S3 and sync with AWS Glue Data Catalog using AWS Wrangler.

        Args:
            data (list[DynamoDBStreamsOutputData]): List of data to be stored and synchronized.
        """
        try:
            # Converting list of DynamoDBStreamsOutputData to DataFrame
            df = pd.DataFrame([tr.__dict__ for tr in data])
        except Exception as e:
            self.logger.error(f"Error converting data to DataFrame: {e}")
            raise

        # Extracting useful information for saving the data
        event_source_service = data[0].event_source_service
        cdc_table_name = f"cdc_{data[0].table_name}"

        # Store DataFrame in S3 (JSON format) and sync with Glue Data Catalog
        try:
            wr.s3.to_json(
                df=df,
                path=f"s3://{self.bucket_name}/{event_source_service}/{cdc_table_name}/",
                index=False,
                dataset=True,
                database=self.data_catalog_database,
                table=cdc_table_name,
                mode="append",
                partition_cols=["event_date"],
                orient="records",
                lines=True
            )

        except wr.exceptions.InvalidTable:
            self.logger.exception(f"The specified table '{cdc_table_name}' is invalid or does not "
                                  "exist in Glue Data Catalog.")
            raise

        except Exception:
            self.logger.exception(f"An unexpected error occurred while storing and syncing data to "
                                  f"S3 and Glue Data Catalog on table '{cdc_table_name}'.")
            raise
