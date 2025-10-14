from typing import Any

from app.src.features.cross.domain.entities.notification_email_info import NotificationEmailInfo
from app.src.features.send_notification_emails.domain.interfaces.email_service_adapter_interface import (
    IEmailServiceAdapter
)
from app.src.features.cross.utils.aws_client import AWSClient
from app.src.features.cross.utils.log import LogUtils


class SESEmailServiceAdapter(IEmailServiceAdapter):
    """
    Implementation of the email service adapter interface using Amazon SES.
    """

    def __init__(self):
        self.logger = LogUtils.setup_logger(__name__)
        self.ses_client = AWSClient.get_client(service_name="ses")
        self.s3_client = AWSClient.get_client(service_name="s3")


    def fetch_email_html_template(self, template_endpoint: str) -> str:
        """
        Fetches the HTML email template from a S3 endpoint.

        Args:
            template_endpoint (str): The endpoint to fetch the HTML template from.

        Returns:
            str: The HTML email template as a string object.
        """
        try:
            # Getting bucket name and object key from S3 endpoint URI
            bucket_name = template_endpoint.split("/")[2]
            object_key = "/".join(template_endpoint.split("/")[3:])
        except Exception as e:
            self.logger.exception("Error getting bucket name and object key from email HTML template "
                                  f"S3 endpoint URI: {template_endpoint}")
            raise e
        
        try:
            # Retrieving email body template from S3
            response = self.s3_client.get_object(
                Bucket=bucket_name,
                Key=object_key
            )
            return response["Body"].read().decode("utf-8")
        except Exception as e:
            self.logger.exception(f"Error fetching email HTML template from S3 endpoint URI {template_endpoint}")
            raise e


    def replace_email_html_template_placeholders(self, template: str, placeholders: dict[str, Any]) -> str:
        """
        Replaces placeholders in the given HTML template with actual values.

        Args:
            template (str | bytes): The HTML email template containing placeholders.
            placeholders (dict): A dictionary mapping placeholders to their actual values.

        Returns:
            str: The HTML email template with placeholders replaced by actual values.
        """
        try:
            for key, value in placeholders.items():
                template = template.replace(f"{{{{{key}}}}}", value)
            return template
        except Exception as e:
            self.logger.exception("Error replacing placeholders in email HTML template")
            raise e


    def send_email(self, email_info: NotificationEmailInfo) -> None:
        """
        Sends an email using the provided email information.

        Args:
            email_info (NotificationEmailInfo): The information needed to send the email.
        """
        if (
            not email_info.template_setup.template_endpoint_url or 
            not email_info.template_setup.template_placeholders
        ):
            raise ValueError("A HTML template endpoint URL and a placeholders dict must be provided to "
                                "generate the email body")

        # Fetching and customizing the HTML email template
        email_template = self.fetch_email_html_template(
            template_endpoint=email_info.template_setup.template_endpoint_url
        )
        email_body = self.replace_email_html_template_placeholders(
            template=email_template,
            placeholders=email_info.template_setup.template_placeholders
        )

        try:
            _ = self.ses_client.send_email(
                Source=email_info.sender,
                Destination={
                    "ToAddresses": email_info.recipients
                },
                Message={
                    "Subject": {
                        "Data": email_info.subject,
                        "Charset": "UTF-8"
                    },
                    "Body": {
                        "Html": {
                            "Data": email_body,
                            "Charset": "UTF-8"
                        }
                    }
                }
            )
        except Exception as e:
            self.logger.exception("Error sending email via Amazon SES with custom HTML template")
            raise e
