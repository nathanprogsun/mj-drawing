import traceback

from app.utils.exception import APPException, HTTPException
from app.utils.json import json_response
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from starlette import status
from starlette.exceptions import HTTPException as StarletteHTTPException


def extract_exception(err: dict) -> str:
    loc, msg, error_type = err["loc"], err["msg"], err["type"]
    error_types = error_type.split(".")
    etype, tag = error_types[0], ".".join(error_types[1:])
    filtered_loc = loc[1:] if loc[0] in ("body", "query", "path") else loc
    field_string = ".".join(map(str, filtered_loc))
    if etype == "value_error":
        if tag == "missing":
            return f"{field_string} is required"
        elif tag == "extra":
            return f"{field_string} is unexpected"
        elif str(tag).startswith("url"):
            return f"{field_string} is not a valid url"
        elif tag == "tuple.length":
            return (
                f'{field_string} must be {err["ctx"]["limit_value"]} '
                f"characters long"
            )
        elif tag == "any_str.min_length":
            return (
                f"{field_string} must be longer than "
                f'{err["ctx"]["limit_value"]}'
            )
        elif tag == "any_str.max_length":
            return (
                f"{field_string} cant be longer than "
                f'{err["ctx"]["limit_value"]}'
            )
        if msg:
            return f"{field_string} error: {msg}"
        return f"{field_string} type error"
    elif etype == "type_error":
        if tag == "not_none":
            return f"{field_string} is not None"
        elif tag == "enum":
            return f"{field_string} is not a valid enumeration member"
        elif tag in ("bool", "byte", "dict"):
            return f"{field_string} value is not a valid {tag} type"
        return f"{field_string} value is not a valid {tag}"
    return f"{field_string} {etype} error: {msg}"


def setup_exception_handler(app: FastAPI):
    @app.exception_handler(APPException)
    async def app_exception_handler(request: Request, exc: APPException):
        return json_response(
            code=exc.code,
            status_code=200,
            data=None,
            message=exc.message,
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        return json_response(
            code=exc.code,
            status_code=exc.code,
            data=None,
            message=exc.message,
        )

    @app.exception_handler(StarletteHTTPException)
    async def starlette_http_exception_handler(
        request: Request, exc: StarletteHTTPException
    ):
        return json_response(
            code=exc.status_code,
            status_code=exc.status_code,
            data=None,
            message=exc.detail,
            headers=exc.headers,
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ):
        msg = []
        for pydantic_error in exc.errors():
            msg.append(extract_exception(pydantic_error))
        traceback.print_exc()

        return json_response(
            code=status.HTTP_400_BAD_REQUEST,
            status_code=status.HTTP_400_BAD_REQUEST,
            data=None,
            message=",".join(msg),
        )

    @app.exception_handler(Exception)
    def generic_exception_handler(request: Request, exc: Exception):
        traceback.print_exc()
        return json_response(
            code=-1,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            data=None,
            message=str(exc),
        )
