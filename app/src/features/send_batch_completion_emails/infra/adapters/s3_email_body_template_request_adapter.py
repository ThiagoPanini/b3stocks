import os

import boto3

from app.src.features.send_batch_completion_emails.domain.interfaces.email_body_template_request_adapter_interface import (
    IEMailBodyTemplateRequestAdapter
)
from app.src.features.send_batch_completion_emails.domain.entities.email_body import EmailBody
from app.src.features.cross.utils.log import LogUtils


class S3MailBodyTemplateAdapter(IEMailBodyTemplateRequestAdapter):
    """
    Implementation of the mail body template adapter interface using Amazon S3.
    """

    def __init__(self):
        self.logger = LogUtils.setup_logger(name=__name__)
        self.client = boto3.client("s3", region_name=boto3.session.Session().region_name)


    def __get_bucket_name_from_s3_uri(self, s3_uri: str) -> str:
        """
        Extracts the bucket name from the given S3 URI.

        Args:
            s3_uri (str): The S3 URI to extract the bucket name from.
        
        Returns:
            str: The extracted bucket name.
        """
        try:
            return s3_uri.split("/")[2]
        except Exception:
            self.logger.exception(f"Error extracting bucket name from S3 URI: {s3_uri}")
            raise

    
    def __get_object_key_from_s3_uri(self, s3_uri: str) -> str:
        """
        Extracts the object key from the given S3 URI.

        Args:
            s3_uri (str): The S3 URI to extract the object key from.

        Returns:
            str: The extracted object key.
        """
        try:
            return "/".join(s3_uri.split("/")[3:])
        except Exception:
            self.logger.exception(f"Error extracting object key from S3 URI: {s3_uri}")
            raise


    def get_email_body_template(self, source_endpoint: str) -> EmailBody:
        """
        Retrieves the email body template from the specified endpoint.

        Args:
            source_endpoint (str): The endpoint to retrieve the email body template from.

        Returns:
            EmailBody: The retrieved email body entity.
        """
        try:
            # Parsing S3 URI and getting bucket name and object key
            bucket_name = self.__get_bucket_name_from_s3_uri(source_endpoint)
            object_key = self.__get_object_key_from_s3_uri(source_endpoint)
        except Exception:
            self.logger.exception(f"Error parsing S3 URI: {source_endpoint}")
            raise

        try:
            # Retrieving email body template from S3
            response = self.client.get_object(
                Bucket=bucket_name,
                Key=object_key
            )
            content = response["Body"].read().decode("utf-8")

            return EmailBody(
                source_endpoint=source_endpoint,
                body_template=content
            )
        except Exception:
            self.logger.exception(f"Error retrieving email body template from {source_endpoint}")
            raise
