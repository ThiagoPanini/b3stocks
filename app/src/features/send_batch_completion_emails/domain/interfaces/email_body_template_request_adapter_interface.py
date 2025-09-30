from abc import ABC, abstractmethod

from app.src.features.send_batch_completion_emails.domain.entities.email_body import EmailBody


class IEMailBodyTemplateRequestAdapter(ABC):
    """
    Interface for requesting email body templates from an endpoint request.
    """

    @abstractmethod
    def get_email_body_template(self, source_endpoint: str) -> EmailBody:
        """
        Retrieves the email body template from the specified endpoint.

        Args:
            source_endpoint (str): The endpoint to retrieve the email body template from.

        Returns:
            EmailBody: The retrieved email body entity.
        """
