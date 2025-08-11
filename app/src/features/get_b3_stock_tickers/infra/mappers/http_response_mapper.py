import json
from typing import Any, Optional
from app.src.features.get_b3_stock_tickers.domain.dtos.output_dto import OutputDTO

class HTTPResponseMapper:
    """
    Maps OutputDTO results to HTTP responses for the presentation layer.
    """

    DEFAULT_HEADERS = {
        "Content-Type": "application/json"
    }

    @staticmethod
    def map(
        output_dto: OutputDTO,
        headers: Optional[dict[str, str]] = DEFAULT_HEADERS
    ) -> dict[str, Any]:
        """
        Maps the output DTO to an HTTP response format.

        Args:
            output_dto (OutputDTO): The output DTO containing the data to be returned.
            headers (Optional[dict[str, str]]): Optional headers for the HTTP response.

        Returns:
            dict[str, Any]: A dictionary representing the HTTP response.
        """

        # Determine status code
        if output_dto.success:
            status_code = 200
        elif output_dto.error:
            # Custom error mapping
            error_msg = output_dto.error.lower()
            if "not found" in error_msg:
                status_code = 404
            elif "unauthorized" in error_msg:
                status_code = 401
            elif "forbidden" in error_msg:
                status_code = 403
            elif "conflict" in error_msg:
                status_code = 409
            elif "bad request" in error_msg:
                status_code = 400
            elif "internal" in error_msg or "exception" in error_msg:
                status_code = 500
            else:
                status_code = 400
        else:
            status_code = 400

        body = json.dumps(output_dto.to_dict())
        return {
            "statusCode": status_code,
            "headers": headers,
            "body": body
        }
