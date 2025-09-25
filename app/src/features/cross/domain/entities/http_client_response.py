from dataclasses import dataclass


@dataclass(frozen=True)
class HTTPClientResponse:
    """
    Represents an HTTP response.

    Attributes:
        url (str): The URL of the request.
        status_code (int): The HTTP status code of the response.
        content (bytes): The content of the response.
        encoding (str): The encoding of the response content.
        elapsed_time (float): The time taken to receive the response in seconds.
    """
    url: str
    status_code: int
    content: bytes
    encoding: str
    elapsed_time: float
