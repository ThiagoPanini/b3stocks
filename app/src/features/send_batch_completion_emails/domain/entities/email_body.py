from dataclasses import dataclass
from typing import Optional


@dataclass
class EmailBody:
    """
    Represents a request to fetch an email body template.

    Args:
        source_endpoint (str): The source endpoint where the template is stored (e.g. S3 URI).
        body_template (bytes): The email body template content in bytes.
        body_rendered (Optional[bytes]): The rendered email body content in bytes, if applicable.
    """
    source_endpoint: str
    body_template: bytes
    body_rendered: Optional[bytes] = None
