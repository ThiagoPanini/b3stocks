from dataclasses import dataclass
from typing import Optional

from app.src.features.send_batch_completion_emails.domain.entities.email_body import EmailBody

@dataclass
class EmailSetup:
    """
    Represents the email setup configuration.

    Args:
        sender (str): The email address of the sender.
        recipients (list[str]): The email addresses of the recipients.
        subject (str): The subject of the email.
        body (Optional[EmailBodyTemplate]): The body of the email, which can be an HTML template.
    """
    sender: str
    recipients: list[str]
    subject: str
    body: Optional[EmailBody] = None
