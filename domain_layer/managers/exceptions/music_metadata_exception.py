import dataclasses as dc
import logging

from domain_layer.managers.exceptions.application_base_exception import (
    ApplicationBaseException,
    LogEvent,
)


class MetadataSteps(LogEvent):
    OpenFile = "Open Music File"
    ReadMetadata = "Read Music Metadata"
    MetadataValidation = "Music Metadata Validation"
    MetadataIngestion = "Ingest Music Metadata"


class MusicMetadataException(ApplicationBaseException):
    def __init__(self, message: str, log_event: LogEvent, data):
        context_data = dc.asdict(data)
        super().__init__(message, log_event, **context_data)

    @property
    def severity(self) -> int:
        return logging.ERROR

    @property
    def reason(self) -> str:
        return "Music metadata processing error"

    @property
    def http_status_code(self) -> int:
        return 400
