import logging
from logging import Logger

from opencensus.ext.azure.log_exporter import AzureLogHandler  # type: ignore

from domain_layer.managers.exceptions.music_metadata_exception import (
    MetadataSteps,
    MusicMetadataException,
)
from domain_layer.managers.loggers.application_logger import ApplicationLogger
from domain_layer.managers.models.music_metadata import MusicMetadata


class DomainFacade:
    def __init__(self, azure_log_handler: AzureLogHandler):
        logger: Logger = logging.getLogger(__name__)
        logger.addHandler(azure_log_handler)
        self.application_logger: ApplicationLogger = ApplicationLogger(logger)

    def process_music_metadata(self, file_path_and_name: str) -> None:
        # ============================================================
        # ============================================================
        # Entry point - Typically a "public" method that is called by a Service Interface Layer (SIL) such as a Web API/gRPC App or an Azure Function App
        # ============================================================
        # ============================================================

        # Step 1: Open Music File
        metadata_step = MetadataSteps.OpenFile
        # Some code doing Step 1
        # Some code doing Step 1

        # Step 2: Read Music Metadata
        metadata_step = MetadataSteps.ReadMetadata
        # Some code doing Step 2
        # Some code doing Step 2
        music_metadata = MusicMetadata(
            title="My Head (Can't Get You Out)",
            artist="Climmer of Blooms",
            album="My Head",
            year=2021,
            track=1,
            genre="Club/Dance, Electronic",
            duration=300,
            filename=file_path_and_name,
        )

        # Step 3: Validate Music Metadata
        metadata_step = MetadataSteps.MetadataValidation
        # Some code doing Step 3
        raise MusicMetadataException(
            message="Vector Database index generation failed for Metadata provided",
            log_event=metadata_step,
            data=music_metadata,
        )

        # Step4: Ingest Music Metadata
        metadata_step = MetadataSteps.MetadataIngestion
        # Some code doing Step 4
        # Some code doing Step 4
