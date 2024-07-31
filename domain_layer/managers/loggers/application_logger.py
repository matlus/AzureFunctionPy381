import inspect
import logging
from typing import Any

from domain_layer.managers.exceptions.application_base_exception import (
    ApplicationBaseException,
)


class ApplicationLogger:
    CUSTOM_DIMENSIONS: str = "custom_dimensions"

    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def log_exception(
        self, exception: Exception, additional_context: "dict[str, Any]" = {}
    ):
        calling_function: str = inspect.stack()[1].function

        if isinstance(exception, ApplicationBaseException):
            self.__log_application_exception(
                exception, additional_context, calling_function
            )
        else:
            self.__log_unhandled_exception(
                exception, additional_context, calling_function
            )

    def __log_application_exception(
        self,
        exception: ApplicationBaseException,
        additional_context: "dict[str, Any]",
        calling_function: str,
    ):
        exception.add_contextual_data(additional_context)

        self.logger.log(
            exception.severity,
            "Application Exception caught in function: '%s' - Message: %s. Contextual Information: %s",
            calling_function,
            exception,
            exception.contextual_data[self.CUSTOM_DIMENSIONS],
            exc_info=exception,
            stack_info=True,
            extra=exception.contextual_data,
        )

    def __log_unhandled_exception(
        self,
        exception: Exception,
        additional_context: "dict[str, Any]",
        calling_function: str,
    ):
        contextual_data: dict[str, dict[str, Any]] = {
            self.CUSTOM_DIMENSIONS: additional_context
        }
        self.logger.log(
            logging.CRITICAL,
            "Unhandled exception caught in function: '%s' - Message: %s. Contextual Information: %s",
            calling_function,
            exception,
            additional_context,
            exc_info=exception,
            stack_info=True,
            extra=contextual_data,
        )

    def log_information(self, message: str, additional_context: "dict[str, Any]"):
        calling_function = inspect.stack()[1].function
        contextual_information = {self.CUSTOM_DIMENSIONS: additional_context}
        self.logger.log(
            logging.INFO,
            "Information logged in function: '%s' - Message: %s. Contextual Information: %s",
            calling_function,
            message,
            additional_context,
            stack_info=False,
            extra=contextual_information,
        )
