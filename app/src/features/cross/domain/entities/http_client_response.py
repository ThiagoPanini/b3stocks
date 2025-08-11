from dataclasses import dataclass


@dataclass(frozen=True)
class HTTPClientResponse:
    """
    Represents an HTTP response.

    Attributes:
        status_code (int): The HTTP status code of the response.
        content (bytes): The content of the response.
    """

    url: str
    status_code: int
    content: bytes
    encoding: str
    elapsed_time: float
