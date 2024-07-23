import json
import logging
from enum import Enum
from typing import Any


class ApplicationBaseExceptionJsonEncoder(json.JSONEncoder):
    def default(self, o: Any):
        if isinstance(o, ApplicationBaseException):
            temp_dict: dict[str, Any] = {"Message": o.message}
            temp_dict.update(
                o.contextual_data[ApplicationBaseException.CUSTOM_DIEMENSIONS]
            )
            return temp_dict

        else:
            return json.JSONEncoder.default(self, o)


class LogEvent(Enum):
    pass


class ApplicationBaseException(Exception):
    CUSTOM_DIEMENSIONS: str = "custom_dimensions"

    severity_levels_dict: "dict[int, str]" = {
        0: "NotSet",
        10: "Debug",
        20: "Information",
        30: "Warning",
        40: "Error",
        50: "Critical",
    }

    def __init__(
        self, message: str, log_event: LogEvent, **context_data: "dict[str, Any]"
    ):
        """Initializes a new instance of the ExceptionBase class.
        message: The error message.
        log_event: The LogEvent step in the process being attempted when the exception occurred.
        context_data: Additional contextual data you want associated with the exception. This data will be included in the custom_dimensions property and logged.
        """
        super().__init__(message)
        self.__message: str = message
        self.__log_event: LogEvent = log_event
        self.__contextual_data: dict[str, dict[str, Any]] = (
            self.__build_contextual_data(context_data.copy())
        )

    def __build_contextual_data(
        self, context_data: "dict[str, Any]"
    ) -> "dict[str, dict[str, Any]]":
        """Builds the contextual_data dictionary with additional context."""
        contextual_data: dict[str, Any] = {
            "LogEvent": self.log_event.value,
            "Severity": self.get_severity_str(self.severity),
            "Reason": self.reason,
            "HttpStatusCode": self.http_status_code,
            **context_data,
        }
        return {self.CUSTOM_DIEMENSIONS: contextual_data}

    @property
    def message(self) -> str:
        return self.__message

    @property
    def log_event(self) -> LogEvent:
        return self.__log_event

    @property
    def contextual_data(self) -> "dict[str, dict[str, Any]]":
        return self.__contextual_data

    def add_contextual_data(self, value: "dict[str, Any]") -> None:
        return self.__contextual_data[self.CUSTOM_DIEMENSIONS].update(value)

    @property
    def severity(self) -> int:
        return logging.ERROR

    @property
    def reason(self) -> str:
        return "An error occurred"

    @property
    def http_status_code(self) -> int:
        return 400

    @staticmethod
    def get_severity_str(severity_level: int) -> str:
        if severity_level in ApplicationBaseException.severity_levels_dict:
            return ApplicationBaseException.severity_levels_dict[severity_level]
        else:
            raise ValueError(
                f"Invalid severity level: {severity_level}. Possible values are 0, 10, 20, 30, 40, 50."
            )
