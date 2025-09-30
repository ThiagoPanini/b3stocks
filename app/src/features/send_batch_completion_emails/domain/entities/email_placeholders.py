from dataclasses import dataclass


@dataclass
class EmailPlaceholders:
    """
    Represents placeholders for email templates.

    Args:
        process_name (str): The name of the process.
        status (str): The status of the process.
        start_time (str): The start time of the process.
        end_time (str): The end time of the process.
        details (str): Additional details about the process.
    """
    process_name: str
    status: str
    start_time: str
    end_time: str
    details: str