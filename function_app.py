import logging

import azure.functions as func
from azure.functions._http import HttpRequestHeaders, HttpResponse
from opencensus.ext.azure.log_exporter import AzureLogHandler  # type: ignore

from domain_layer.domain_facade import DomainFacade
from domain_layer.managers.loggers.application_logger import (
    ApplicationLogger,  # type: ignore
)
from middleware.exception_to_http_translator import ExceptionToHttpResponseTranslator

logger = logging.getLogger(__name__)
azure_log_handler = AzureLogHandler()
logger.addHandler(azure_log_handler)
application_logger = ApplicationLogger(logger)
domain_facade = DomainFacade(azure_log_handler)

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)


def ensure_required_headers(http_request_headers: HttpRequestHeaders) -> None:
    spanId = http_request_headers.get("span_id")  # type: ignore
    if spanId is None:
        raise Exception(
            "span_id HTTP header is missing. This is a required HTTP Header."
        )


@app.route(route="http_trigger")
def http_trigger(req: func.HttpRequest, context: func.Context) -> HttpResponse:
    application_logger.log_information(
        "http_trigger function processed a request.",
        {"additionalData1": "Value1", "additionalData2": 43},
    )

    try:
        ensure_required_headers(req.headers)
        # raise ValueError("There is a problem with the value")
        domain_facade.process_music_metadata("C:\\somefilepath.mp3")
        return func.HttpResponse("All good", status_code=200)
    except Exception as e:
        application_logger.log_exception(
            e,
            {
                "FunctionName": context.function_name,
                "SpanId": get_span_id(req.headers),
                "invocationid": context.invocation_id,
            },
        )
        return ExceptionToHttpResponseTranslator.translate(e, func.HttpResponse)


def get_span_id(http_request_headers: HttpRequestHeaders) -> str:
    return http_request_headers.get("span_id") or "00000000-0000-0000-0000-000000000000"  # type: ignore
