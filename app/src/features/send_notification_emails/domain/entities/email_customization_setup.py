from dataclasses import dataclass
from typing import Optional, Any


@dataclass
class EmailCustomizationSetup:
    """
    Represents the setup for customizing an email.

    Attributes:
        use_custom_html_template (bool): Whether to use a custom HTML template for the email body.
        html_template_endpoint_url (Optional[str]): The endpoint URL of the custom HTML template.
        html_template_placeholders (Optional[dict[str, Any]]): Placeholders to replace in the custom HTML template.
    """
    use_custom_html_template: bool
    html_template_endpoint_url: Optional[str] = None
    html_template_placeholders: Optional[dict[str, Any]] = None