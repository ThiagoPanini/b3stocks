from abc import ABC, abstractmethod
from typing import Any

from app.src.features.cross.domain.entities.notification_email_info import NotificationEmailInfo


class IEmailServiceAdapter(ABC):
    """
    Interface for an email service adapter.
    """

    @abstractmethod
    def fetch_email_html_template(self, template_endpoint: str) -> str:
        """
        Fetches the HTML email template from the given endpoint.

        Args:
            template_endpoint (str): The endpoint to fetch the HTML template from.

        Returns:
            str: The HTML email template as a string object.
        """


    @abstractmethod
    def replace_email_html_template_placeholders(self, template: str, placeholders: dict[str, Any]) -> str:
        """
        Replaces placeholders in the given HTML template with actual values.

        Args:
            template (str | bytes): The HTML email template containing placeholders.
            placeholders (dict): A dictionary mapping placeholders to their actual values.

        Returns:
            str | bytes: The HTML email template with placeholders replaced by actual values.
        """


    @abstractmethod
    def send_email(self, email_info: NotificationEmailInfo) -> None:
        """
        Sends an email using the provided email information.

        Args:
            email_info (NotificationEmailInfo): The information needed to send the email.
        """
