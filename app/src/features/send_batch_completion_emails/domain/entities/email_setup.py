from dataclasses import dataclass
from typing import Optional

from app.src.features.send_batch_completion_emails.domain.entities.email_body import EmailBody

@dataclass
class EmailSetup:
    """
    Represents the email setup configuration.

    Args:
        sender (str): The email address of the sender.
        recipient (str): The email address of the recipient.
        subject (str): The subject of the email.
        body (Optional[EmailBodyTemplate]): The body of the email, which can be an HTML template.
    """
    sender: str
    recipient: str
    subject: str
    body: Optional[EmailBody] = None
