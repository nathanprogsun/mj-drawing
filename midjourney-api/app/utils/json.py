from datetime import datetime
from typing import Any, Dict, List, Optional, Union
from zoneinfo import ZoneInfo

import orjson
from app.utils.enums import BusinessCode, HTTPMessage
from app.utils.response import Response
from starlette import status
from starlette.responses import JSONResponse


class APIResponse(JSONResponse):
    media_type = "application/json"

    def render(self, content: Any) -> bytes:
        assert (
            orjson is not None
        ), "orjson must be installed to use ORJSONResponse"
        return orjson.dumps(
            content,
            option=orjson.OPT_NON_STR_KEYS | orjson.OPT_SERIALIZE_NUMPY,
        )


def json_response(
    *,
    code=BusinessCode.NO_ERROR,
    status_code=status.HTTP_200_OK,
    data: Optional[Union[List, Dict]],
    message=HTTPMessage.SUCCESS.value,
    headers: Optional[Dict] = None,
):
    dict_func = getattr(data, "dict", None)
    if dict_func and callable(dict_func):
        data = data.dict()
    resp = APIResponse(
        status_code=status_code,
        content=Response(
            code=code,
            message=message,
            data=data,
        ).dict(),
        headers=headers,
    )
    return resp


def orjson_dumps(v, *, default):
    # orjson.dumps returns bytes,
    # to match standard json.dumps we need to decode
    try:
        return orjson.dumps(v, default=default).decode()
    except TypeError as e:
        if str(e) == "Integer exceeds 64-bit range":
            import json

            return json.dumps(v, default=default)
        raise e


def convert_datetime_to_gmt(dt: datetime) -> str:
    if not dt.tzinfo:
        dt = dt.replace(tzinfo=ZoneInfo("UTC"))

    return dt.strftime("%Y-%m-%dT%H:%M:%S%z")


json_loads = orjson.loads
json_dumps = orjson_dumps
