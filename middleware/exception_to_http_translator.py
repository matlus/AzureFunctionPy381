import json
from typing import Type

from azure.functions._http import HttpResponse

from domain_layer.managers.exceptions.application_base_exception import (
    ApplicationBaseException,
    ApplicationBaseExceptionJsonEncoder,
)


class ExceptionToHttpResponseTranslator:
    @staticmethod
    def translate(e: Exception, http_response: Type[HttpResponse]) -> HttpResponse:
        if isinstance(e, ApplicationBaseException):
            return http_response(
                json.dumps(e, cls=ApplicationBaseExceptionJsonEncoder),
                status_code=e.http_status_code,
                headers={
                    "Content-Type": "application/json",
                    "reason": e.reason,
                    "X-Exception-Type": f"{type(e).__name__}",
                },
            )
        else:
            return http_response(
                json.dumps(
                    {
                        "Message": "An unhandled exception occurred. Please contact support."
                    }
                ),
                status_code=500,
                headers={
                    "Content-Type": "application/json",
                    "reason": "Unhandled Exception",
                    "X-Exception-Type": f"{type(e).__name__}",
                },
            )
