from typing import Any

import boto3

from app.src.features.send_batch_completion_emails.domain.interfaces.email_service_adapter_interface import (
    IEmailServiceAdapter
)
from app.src.features.send_batch_completion_emails.domain.entities.email_setup import EmailSetup
from app.src.features.cross.domain.entities.batch_process import BatchProcess
from app.src.features.cross.utils.log import LogUtils


logger = LogUtils.setup_logger(__name__)


class SESMailServiceAdapter(IEmailServiceAdapter):
    """
    Implementation of the mail service adapter interface using Amazon SES.
    """
    
    def __init__(self):
        self.client = boto3.client("ses", region_name=boto3.session.Session().region_name)


    def __replace_placeholders(self, template: str, placeholders: dict) -> str:
        """
        Replaces placeholders in the given template with actual values.

        Args:
            template (str): The email template containing placeholders.
            placeholders (dict): A dictionary mapping placeholders to their actual values.

        Returns:
            str: The email template with placeholders replaced by actual values.
        """
        for key, value in placeholders.items():
            template = template.replace(f"{{{{{key}}}}}", value)
        return template


    def send_email(
        self,
        email_setup: EmailSetup,
        replace_placeholders: bool = False,
        placeholders: dict[str, Any] = None
    ) -> None:
        """
        Sends a HTML email using the mail service.

        Args:
            email_setup (EmailConfig): The email configuration containing sender, recipient, subject, and body.
            replace_placeholders (bool): Whether to replace placeholders in the email body.
            placeholders (dict): A dictionary of placeholders to replace in the email body.
        """
        if replace_placeholders and placeholders:
            try:
                email_setup.body.body_template = self.__replace_placeholders(
                    email_setup.body.body_template,
                    placeholders
                )
            except Exception:
                logger.exception("Failed to replace placeholders in email body")
                raise
        try:
            _ = self.client.send_email(
                Source=email_setup.sender,
                Destination={"ToAddresses": email_setup.recipients},
                Message={
                    "Subject": {
                        "Data": email_setup.subject,
                        "Charset": "UTF-8"
                    },
                    "Body": {
                        "Html": {
                            "Data": email_setup.body.body_template,
                            "Charset": "UTF-8"
                        }
                    }
                }
            )
        except Exception:
            logger.exception("Failed to send email via SES")
            raise
