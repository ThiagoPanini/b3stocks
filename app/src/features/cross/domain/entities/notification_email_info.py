from dataclasses import dataclass

from app.src.features.cross.domain.entities.notification_email_template_setup import (
    NotificationEmailTemplateSetup
)


@dataclass
class NotificationEmailInfo:
    """
    Represents the information needed to send a notification email.

    Attributes:
        sender (str): The email address of the sender.
        recipients (list[str]): A list of recipient email addresses.
        subject (str): The subject of the email.
        template_setup (Optional[EmailHTMLTemplateSetup]): An optional setup for the HTML template.
    """
    sender: str
    recipients: list[str]
    subject: str
    template_setup: NotificationEmailTemplateSetup
