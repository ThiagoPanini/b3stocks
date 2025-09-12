from dataclasses import dataclass

from app.src.features.stream_cdc_data.domain.entities.event_record import EventRecord


@dataclass
class StreamCDCDataInputDTO:
    """
    Data Transfer Object for input data from AWS Lambda event.
    """
    records: list[EventRecord]