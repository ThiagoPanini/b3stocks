from abc import ABC, abstractmethod
from typing import Any

from app.src.features.send_notification_emails.domain.entities.email_info import EmailInfo


class IEmailServiceAdapter(ABC):
    """
    Interface for an email service adapter.
    """

    @abstractmethod
    def fetch_email_html_template(self, endpoint: str) -> str:
        """
        Fetches the HTML email template from the given endpoint.

        Args:
            endpoint (str): The endpoint to fetch the HTML template from.

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
    def send_email(
        self,
        email_info: EmailInfo,
        use_custom_html_template: bool = False,
        html_template_endpoint_url: str = None,
        html_template_placeholders: dict[str, Any] = None
    ) -> None:
        """
        Sends an email using the provided email information.

        Args:
            email_info (EmailInfo): The information needed to send the email.
            use_custom_html_template (bool): Whether to use a custom HTML template for the email body.
            html_template_endpoint_url (str): The endpoint URL of the custom HTML template.
            html_template_placeholders (dict[str, Any]): Placeholders to replace in the custom HTML template.
        """
