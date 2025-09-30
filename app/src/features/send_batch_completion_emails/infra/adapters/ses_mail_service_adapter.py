from app.src.features.send_batch_completion_emails.domain.interfaces.email_service_adapter_interface import (
    IEmailServiceAdapter
)

from app.src.features.send_batch_completion_emails.domain.entities.email_setup import EmailSetup
from app.src.features.cross.domain.entities.batch_process import BatchProcess


class SESMailServiceAdapter(IEmailServiceAdapter):
    """
    Implementation of the mail service adapter interface using Amazon SES.
    """

    def send_email(self, email_config: EmailSetup, batch_process: BatchProcess) -> None:
        """
        Sends an email using the mail service.

        Args:
            email_config (EmailConfig): The email configuration containing sender, recipient, subject, and body.
            batch_process (BatchProcess): The batch process information.
        """
        raise NotImplementedError("Method not implemented yet.")
