from dataclasses import dataclass
from typing import Optional, Any


@dataclass
class NotificationEmailTemplateSetup:
    """
    Represents the setup for customizing a notification email.

    Attributes:
        template_endpoint_url (Optional[str]): The endpoint URL of the custom HTML template.
        template_placeholders (Optional[dict[str, Any]]): Placeholders to replace in the custom HTML template.
    """
    template_endpoint_url: Optional[str] = None
    template_placeholders: Optional[dict[str, Any]] = None
