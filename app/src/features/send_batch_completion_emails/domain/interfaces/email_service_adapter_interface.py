from abc import ABC, abstractmethod

from app.src.features.send_batch_completion_emails.domain.entities.email_setup import EmailSetup
from app.src.features.cross.domain.entities.batch_process import BatchProcess


class IEmailServiceAdapter(ABC):
    """
    Interface for sending emails using a mail service (e.g., SES).
    """

    @abstractmethod
    def send_email(self, email_config: EmailSetup, batch_process: BatchProcess) -> None:
        """
        Sends an email using the mail service.

        Args:
            email_config (EmailSetup): The email configuration containing sender, recipient, subject, and body.
            batch_process (BatchProcess): The batch process information.
        """
