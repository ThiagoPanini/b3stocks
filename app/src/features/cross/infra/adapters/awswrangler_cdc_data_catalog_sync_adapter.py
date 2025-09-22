import os
from datetime import datetime, UTC

import boto3
import awswrangler as wr
import pandas as pd

from app.src.features.cross.domain.interfaces.cdc_data_catalog_sync_adapter_interface import (
    ICDCDataCatalogSyncAdapter
)
from app.src.features.cross.domain.entities.dynamodb_streams_output_data import (
    DynamoDBStreamsOutputData
)

from app.src.features.cross.utils.log import LogUtils
from app.src.features.cross.utils.date_and_time import DateAndTimeUtils
from app.src.features.cross.value_objects import (
    Timezone,
    DateFormat
)


class AWSWranglerCDCDataCatalogSyncAdapter(ICDCDataCatalogSyncAdapter):
    """
    Implementation of ICDCDataCatalogSyncAdapter to store and sync from a database streams source
    with a catalog using AWS Wrangler.
    """

    def __init__(self):
        self.logger = LogUtils.setup_logger(name=__name__)
        self.cdc_bucket_name_prefix = os.getenv("S3_ANALYTICS_CDC_BUCKET_NAME_PREFIX")
        self.sor_bucket_name_prefix = os.getenv("S3_ANALYTICS_SOR_BUCKET_NAME_PREFIX")
        self.cdc_data_catalog_database = os.getenv("DATA_CATALOG_CDC_DATABASE_NAME")
        self.sor_data_catalog_database = os.getenv("DATA_CATALOG_SOR_DATABASE_NAME")
        self.bucket_names = self.__build_bucket_names()


    def __build_bucket_names(self) -> dict:
        """
        Builds the S3 bucket names for both CDC and SoR data.

        Returns:
            A dictionary containing the bucket names.
        """
        region = boto3.session.Session().region_name
        account_id = boto3.client("sts").get_caller_identity().get("Account")

        return {
            "cdc": f"{self.cdc_bucket_name_prefix}-{account_id}-{region}",
            "sor": f"{self.sor_bucket_name_prefix}-{account_id}-{region}"
        }


    def store_and_sync_cdc_data(self, data: list[DynamoDBStreamsOutputData]) -> None:
        """
        Adapter to store CDC data in S3 and sync with AWS Glue Data Catalog using AWS Wrangler.

        Args:
            data (list[DynamoDBStreamsOutputData]): List of CDC data to be stored and synchronized.
        """
        try:
            # Converting list of DynamoDBStreamsOutputData to DataFrame
            df = pd.DataFrame([tr.__dict__ for tr in data])
        except Exception:
            self.logger.exception(f"Error converting event data to DataFrame")
            raise

        # Extracting useful information for saving the data
        event_source_service = data[0].event_source_service
        cdc_table_name = f"cdc_{data[0].table_name}"

        # Store DataFrame in S3 (JSON format) and sync with Glue Data Catalog
        try:
            wr.s3.to_json(
                df=df,
                path=f"s3://{self.bucket_names['cdc']}/{event_source_service}/{cdc_table_name}/",
                index=False,
                dataset=True,
                database=self.cdc_data_catalog_database,
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

    
    def store_and_sync_sor_data(self, data: list[DynamoDBStreamsOutputData]) -> None:
        """
        Adapter to store raw data taken from the CDC source in S3 and sync with AWS Glue Data
        Catalog using AWS Wrangler.

        Args:
            data (list[DynamoDBStreamsOutputData]): List of data to be stored and synchronized.
        """
        try:
            # Taken the new image (updated raw data) from each record and converting to DataFrame
            df = pd.DataFrame([tr.table_new_image for tr in data])

            # Adding execution timestamp and date columns for 
            df["execution_timestamp"] = DateAndTimeUtils.datetime_now(
                timezone=Timezone.SAO_PAULO
            )
            df["execution_date"] = DateAndTimeUtils.datetime_now_str(
                timezone=Timezone.SAO_PAULO,
                format=DateFormat.DATE
            )

        except Exception:
            self.logger.exception(f"Error converting new image data to DataFrame")
            raise

        sor_table_name = f"sor_{data[0].table_name}"

        # Store DataFrame in S3 (Parquet format) and sync with Glue Data Catalog
        try:
            wr.s3.to_parquet(
                df=df,
                path=f"s3://{self.bucket_names['sor']}/{sor_table_name}/",
                index=False,
                dataset=True,
                database=self.sor_data_catalog_database,
                table=sor_table_name,
                mode="append",
                compression="snappy",
                partition_cols=["execution_date"]
            )

        except wr.exceptions.InvalidTable:
            self.logger.exception(f"The specified table '{sor_table_name}' is invalid or does not "
                                  "exist in Glue Data Catalog.")
            raise

        except Exception:
            self.logger.exception(f"An unexpected error occurred while storing and syncing data to "
                                  f"S3 and Glue Data Catalog on table '{sor_table_name}'.")
            raise
