from abc import ABC, abstractmethod

from app.src.features.send_batch_completion_emails.domain.entities.email_setup import EmailSetup


class IEmailServiceAdapter(ABC):
    """
    Interface for sending emails using a mail service (e.g., SES).
    """

    @abstractmethod
    def send_email(self, email_setup: EmailSetup) -> None:
        """
        Sends an email using the mail service.

        Args:
            email_setup (EmailSetup): The email configuration containing sender, recipient, subject, and body.
        """
