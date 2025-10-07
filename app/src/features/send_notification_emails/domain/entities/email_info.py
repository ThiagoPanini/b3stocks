from dataclasses import dataclass
from typing import Optional

from app.src.features.send_notification_emails.domain.entities.email_customization_setup import (
    EmailCustomizationSetup
)


@dataclass
class EmailInfo:
    """
    Represents the information needed to send an email.

    Attributes:
        sender (str): The email address of the sender.
        recipients (list[str]): A list of recipient email addresses.
        subject (str): The subject of the email.
        body (str): The body content of the email.
        html_template_endpoint (Optional[str]): An optional endpoint for fetch a HTML template.
    """
    sender: str
    recipients: list[str]
    subject: str
    body: Optional[str]
    customization: EmailCustomizationSetup
