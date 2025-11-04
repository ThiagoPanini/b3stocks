from abc import ABC, abstractmethod
from typing import Any, Optional

from app.src.features.send_batch_completion_emails.domain.entities.email_setup import (
    EmailSetup
)


class IEmailServiceAdapter(ABC):
    """
    Interface for sending emails using a mail service (e.g., SES).
    """

    @abstractmethod
    def send_email(
        self,
        email_setup: EmailSetup,
        replace_placeholders: bool = False,
        placeholders: Optional[dict[str, Any]] = None
    ) -> None:
        """
        Sends an email using the mail service.

        Args:
            email_setup (EmailSetup): The email configuration containing
                sender, recipient, subject, and body.
            replace_placeholders (bool): Whether to replace placeholders in
                the email body.
            placeholders (dict): A dictionary of placeholders to replace in
                the email body.
        """
