from datetime import datetime

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel as PydanticBaseModel
from pydantic import root_validator

from .json import convert_datetime_to_gmt, json_dumps, json_loads


class BaseModel(PydanticBaseModel):
    class Config:
        json_loads = json_loads
        json_dumps = json_dumps
        json_encoders = {
            datetime: convert_datetime_to_gmt
        }  # method for customer JSON encoding of datetime fields

    @root_validator()
    def set_null_microseconds(cls, data: dict) -> dict:
        """Drops microseconds in all the datetime field values."""
        datetime_fields = {
            k: v.replace(microsecond=0)
            for k, v in data.items()
            if isinstance(k, datetime)
        }
        return {**data, **datetime_fields}

    def serializable_dict(self, **kwargs):
        """Return a dict which contains only serializable fields."""
        default_dict = super().dict(**kwargs)
        return jsonable_encoder(default_dict)
